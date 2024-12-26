import stripe
from rest_framework.decorators import api_view
import stripe.error
import stripe.webhook
from property.serializers import BookingSerializer
from django.http import JsonResponse
from .models import UserPayment
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from property.models import Property, Reservation
from .tasks import send_invoice_creation_message
from drf_yasg.utils import swagger_auto_schema
from .swagger_usecases import payment_success_response, payment_cancel_response, stripe_webhook_response

import logging



logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_summary="Handle Successful Payments",
    operation_description="Retrieve details about a successful Stripe payment, including reservation and customer information.",
    responses={200: payment_success_response, 400: "Bad Request", 404: "Not Found"}
)
@api_view(['GET'])
def payment_success(request):
    try:
        # Retrieve session ID from query parameters
        checkout_session_id = request.GET.get('session_id', None)
        if not checkout_session_id:
            return JsonResponse({'success': False, 'error': 'Missing session_id'}, status=400)

        # Retrieve the Stripe session
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer_id = session.customer
        customer = stripe.Customer.retrieve(customer_id)

        # Use metadata to get booking details
        metadata = {
            'pk': session.metadata['property_id'],
            'start_date': session.metadata['start_date'],
            'end_date': session.metadata['end_date'],
            'total_price': session.metadata['total_price'],
            'number_of_nights': session.metadata['number_of_nights'],
            'guests': session.metadata['guests'],
            'has_paid': session.metadata.get('has_paid', False)
        }

        # Validate metadata using BookingSerializer
        serializer = BookingSerializer(data=metadata)
        if not serializer.is_valid():
            return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)

        # Retrieve the property
        property = Property.objects.get(pk=metadata['pk'])

        # Create the reservation
        reservation = Reservation.objects.create(
            property=property,
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
            number_of_nights=serializer.validated_data['number_of_nights'],
            total_price=serializer.validated_data['total_price'],
            guests=serializer.validated_data['guests'],
            has_paid=serializer.validated_data.get('has_paid', False),
            stripe_checkout_id=checkout_session_id,
            created_by=request.user
        )

        # Prepare response
        response_data = {
            "success": True,
            "reservation": {
                "id": reservation.id,
                "start_date": reservation.start_date,
                "end_date": reservation.end_date,
                "total_price": float(reservation.total_price),
                "number_of_nights": reservation.number_of_nights,
                "guests": reservation.guests,
                'has_paid': reservation.has_paid,
                "created_by": request.user.name,
                "property": {
                    "id": property.id,
                    "name": property.title,
                    "address": property.country,
                    "image_url": property.image_url(),
                },
            },
            "customer": {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
            },
        }
        send_invoice_creation_message.delay(response_data)

        return JsonResponse(response_data, status=200)

    except Property.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Property not found'}, status=404)

    except Exception as e:
        logger.error('Error:', e)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@swagger_auto_schema(
    method="get",
    operation_summary="Handle Canceled Payments",
    operation_description="Indicate that a payment was canceled.",
    responses={200: payment_cancel_response}
)
@api_view(['GET'])
def payment_cancel(request, pk):
    return JsonResponse({'success': False, 'message': 'Payment was canceled'})

@swagger_auto_schema(
    method="post",
    operation_summary="Stripe Webhook Handler",
    operation_description="Process Stripe webhook events, including payment completions.",
    responses={200: stripe_webhook_response, 400: "Bad Request"}
)
@require_POST
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    signature_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    # Verify webhook signature
    try:
        event = stripe.Webhook.construct_event(payload, signature_header, endpoint_secret)
    except stripe.error as e:
        logger.error(f"Signature verification failed: {e}")
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return JsonResponse({'error': 'Webhook error'}, status=400)

    # Handle the 'checkout.session.completed' event
    session = event['data']['object']
    reservation_id = session.metadata.get('reservation_id')
    if reservation_id:
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.has_paid = True
            reservation.save()
        except Reservation.DoesNotExist:
            logger.warning(f"Reservation not found for ID: {reservation_id}")
            return JsonResponse({'error': 'Reservation not found'}, status=404)

    return JsonResponse({'status': 'success'}, status=200)