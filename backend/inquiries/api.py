from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from .models import Inquiry
from useraccounts.models import User
from rest_framework.parsers import JSONParser
from django.http import Http404
from .serializers import CreateInquirySerializer, GetInquirySerializer, MessageSerializer, UpdateStatusSerializer, AssignInquirySerializer, CustomerServiceAgentSerializer
from drf_yasg.utils import swagger_auto_schema
from .swagger_usecases import (create_inquiry_request_schema, 
create_inquiry_response_schema, update_status_request_schema,
update_status_response_schema, add_message_request_schema, add_message_response_schema, get_inquiries_response_schema)
import logging

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method="post",
    operation_summary="Create an Inquiry",
    operation_description="Allows a user to submit a new inquiry with a subject, message, and email.",
    request_body=create_inquiry_request_schema,
    responses={201: create_inquiry_response_schema, 400: "Validation Error", 500: "Server Error"}
)
@api_view(['POST'])
def create_inquiry(request):
    try:
        serializer = CreateInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse(e, status=500)
    
@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve Inquiries",
    operation_description="Retrieves all inquiries for the current user based on their role and optional query parameters (status, queue).",
    responses={200: get_inquiries_response_schema, 500: "Server Error"}
)
@api_view(['GET'])
def inquiries_view(request):
    if request.user.role == User.RoleChoises.ADMIN:
        inquiries = Inquiry.objects.all()
    elif request.user.role == User.RoleChoises.CUSTOMER_SERVICE:
        inquiries = Inquiry.objects.filter(customer_service=request.user, is_assigned_to_customer_service=True).select_related('user', 'customer_service')
    else:
        inquiries = Inquiry.objects.filter(user=request.user)
    logger.debug(f"Requesting User: {request.user.email}, Role: {request.user.role}, user: {request.user}")
    print(f"Requesting User: {request.user.email}, Role: {request.user.role}: {list(inquiries)}, user: {request.user}")
    status = request.query_params.get('status')  # e.g., "active", "pending", "resolved"
    in_queue = request.query_params.get('queue')  # e.g., "true" for unassigned inquiries

    if status:
        inquiries = inquiries.filter(status=status)  # Assuming status values are stored as uppercase enums
    if in_queue:
        inquiries = inquiries.filter(is_assigned_to_customer_service=False)

    # Order the results
    inquiries = inquiries.order_by('-created_at')

    inquiries_serializer = GetInquirySerializer(inquiries, many=True)
    return JsonResponse(inquiries_serializer.data, safe=False)


@swagger_auto_schema(
    method="post",
    operation_summary="Add a Message",
    operation_description="Allows a user or customer service agent to add a message to an existing inquiry.",
    request_body=add_message_request_schema,
    responses={201: add_message_response_schema, 400: "Validation Error", 404: "Inquiry Not Found"}
)
@api_view(['POST'])
def add_message(request, pk):
    try:
        inquiry = Inquiry.objects.get(pk=pk)
        data = request.data  # Expecting 'sender' and 'message'
        serializer = MessageSerializer(data=data)

        if serializer.is_valid():
            message = serializer.save(inquiry=inquiry)  # Link message to inquiry
            return JsonResponse(MessageSerializer(message).data, status=201)
        return JsonResponse(serializer.errors, status=400)

    except Inquiry.DoesNotExist:
        return JsonResponse({"error": "Inquiry not found"}, status=404)
    

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def assign_inquiry(request, inquiry_id):
    try:
        inquiry = Inquiry.objects.get(id=inquiry_id)
    except Inquiry.DoesNotExist:
        return JsonResponse({'error': 'Inquiry not found'}, status=404)

    # Ensure customer_service is provided
    customer_service_id = request.data.get('customer_service')
    if not customer_service_id:
        return JsonResponse({'error': 'Customer service agent is required'}, status=400)

    try:
        customer_service = User.objects.get(id=customer_service_id, role=User.RoleChoises.CUSTOMER_SERVICE)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Customer service agent not found'}, status=404)

    inquiry.customer_service = customer_service
    inquiry.is_assigned_to_customer_service = True
    inquiry.status = Inquiry.StatusChoice.IN_PROGRESS
    inquiry.save()

    return JsonResponse({'success': 'Inquiry successfully assigned to agent'}, status=200)

@api_view(['GET'])
def get_customer_service_agents(request):
    qs = User.objects.filter(role=User.RoleChoises.CUSTOMER_SERVICE)
    serializer = CustomerServiceAgentSerializer(qs, many=True)
    logger.debug("Serialized Data:", serializer.data)  # Log the serialized data
    return JsonResponse(serializer.data, safe=False)


@swagger_auto_schema(
    method="put",
    operation_summary="Update Inquiry Status",
    operation_description="Updates the status of an inquiry (e.g., active, pending, resolved) and marks it as resolved if applicable.",
    request_body=update_status_request_schema,
    responses={200: update_status_response_schema, 400: "Validation Error", 404: "Inquiry Not Found"}
)
@api_view(['PUT'])
def update_inquiry_status(request, pk):
    try:
        inquiry = Inquiry.objects.get(pk=pk)
        data = JSONParser().parse(request)
        if data.get('status') == 'resolved':
            data['is_resolved'] = True
        serializer = UpdateStatusSerializer(inquiry, data=data, partial=True)  # partial=True allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    except Inquiry.DoesNotExist:
        return JsonResponse({"error": "Inquiry not found"}, status=404)
    


@api_view(['GET'])
def get_inquiry(request, pk):
    try:
        requsting_user = request.user
        inquiry = Inquiry.objects.get(pk=pk)
        serializer = GetInquirySerializer(inquiry)
        response_data = serializer.data
        response_data['user_role'] = requsting_user.role
        return JsonResponse(response_data, status=200)
    except Inquiry.DoesNotExist:
        return JsonResponse({"error": "Inquiry not found"}, status=404)