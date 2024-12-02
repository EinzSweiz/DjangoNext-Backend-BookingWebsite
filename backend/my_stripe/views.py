from django.shortcuts import render
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def product_checkout_view(request, property, pk, total_price, start_date, end_date, number_of_nights, guests, has_paid):
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',  # You can change the currency
                        'product_data': {
                            'name': property.title,
                        },
                        'unit_amount': int(float(total_price) * 100),  # Stripe expects amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            payment_method_types=['card'],
            customer_creation='always',
            success_url='http://165.22.76.137/payment/success?session_id={CHECKOUT_SESSION_ID}',  # Redirect to success URL after payment  # Redirect to success URL after payment
            cancel_url=request.build_absolute_uri(f'/payment/cancel/{pk}/'),  # Redirect to cancel URL if payment fails
            customer_email=request.user.email,  # Optional: Prefill user email in checkout
            metadata={
                'property_id': pk,
                'start_date': start_date,
                'end_date': end_date,
                'number_of_nights': number_of_nights,
                'guests': guests,
                'total_price': total_price,
                'has_paid': has_paid,
            }
        )
    return checkout_session