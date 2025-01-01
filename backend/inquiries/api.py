from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Inquiry, Message
from useraccounts.models import User
from .serializers import (
    CreateInquirySerializer,
    GetInquirySerializer,
    MessageSerializer,
    UpdateStatusSerializer,
    UserModelDynamicSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from .swagger_usecases import (
    create_inquiry_request_schema,
    create_inquiry_response_schema,
    update_status_request_schema,
    update_status_response_schema,
    add_message_request_schema,
    add_message_response_schema,
    get_inquiries_response_schema,
    get_inquiry_response_schema,
    get_customer_service_agents_response_schema,
)
import logging

logger = logging.getLogger(__name__)

class CreateInquiryAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Create an Inquiry",
        operation_description="Allows a user to submit a new inquiry with a subject, message, and email.",
        request_body=create_inquiry_request_schema,
        responses={201: create_inquiry_response_schema, 400: "Validation Error", 500: "Server Error"}
    )
    def post(self, request):
        serializer = CreateInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class InquiriesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve Inquiries",
        operation_description="Retrieves all inquiries for the current user based on their role and optional query parameters (status, queue).",
        responses={200: get_inquiries_response_schema, 500: "Server Error"}
    )
    def get(self, request):
        if request.user.role == User.RoleChoises.ADMIN:
            inquiries = Inquiry.objects.all()
        elif request.user.role == User.RoleChoises.CUSTOMER_SERVICE:
            inquiries = Inquiry.objects.filter(customer_service=request.user, is_assigned_to_customer_service=True).select_related('user', 'customer_service')
        else:
            inquiries = Inquiry.objects.filter(user=request.user)

        status = request.query_params.get('status')
        in_queue = request.query_params.get('queue')

        if status:
            inquiries = inquiries.filter(status=status)
        if in_queue:
            inquiries = inquiries.filter(is_assigned_to_customer_service=False)

        inquiries = inquiries.order_by('-created_at')
        serializer = GetInquirySerializer(inquiries, many=True)
        return JsonResponse(serializer.data, safe=False)


class AddMessageAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Add a Message",
        operation_description="Allows a user or customer service agent to add a message to an existing inquiry.",
        request_body=add_message_request_schema,
        responses={201: add_message_response_schema, 400: "Validation Error", 404: "Inquiry Not Found"}
    )
    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(inquiry=inquiry)
            return JsonResponse(MessageSerializer(message).data, status=201)
        return JsonResponse(serializer.errors, status=400)


class AssignInquiryAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, inquiry_id):
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)
        customer_service_id = request.data.get('customer_service')
        if not customer_service_id:
            return JsonResponse({'error': 'Customer service agent is required'}, status=400)

        customer_service = get_object_or_404(User, id=customer_service_id, role=User.RoleChoises.CUSTOMER_SERVICE)
        inquiry.customer_service = customer_service
        inquiry.is_assigned_to_customer_service = True
        inquiry.status = Inquiry.StatusChoice.IN_PROGRESS
        inquiry.save()
        return JsonResponse({'success': 'Inquiry successfully assigned to agent'}, status=200)


class GetCustomerServiceAgentsAPIView(APIView):
    """
    Retrieve a list of all customer service agents.
    """
    @swagger_auto_schema(
        operation_summary="Get Customer Service Agents",
        operation_description="Fetch a list of all customer service agents, including their ID, name, and email.",
        responses={200: get_customer_service_agents_response_schema},
    )
    def get(self, request):
        agents = User.objects.filter(role=User.RoleChoises.CUSTOMER_SERVICE)
        serializer = UserModelDynamicSerializer(agents, fields=['id', 'name', 'email'], many=True)
        return JsonResponse(serializer.data, safe=False)


class UpdateInquiryStatusAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Update Inquiry Status",
        operation_description="Updates the status of an inquiry (e.g., active, pending, resolved) and marks it as resolved if applicable.",
        request_body=update_status_request_schema,
        responses={200: update_status_response_schema, 400: "Validation Error", 404: "Inquiry Not Found"}
    )
    def put(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        data = request.data
        if data.get('status') == 'resolved':
            data['is_resolved'] = True
        serializer = UpdateStatusSerializer(inquiry, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)


class GetInquiryAPIView(APIView):
    """
    Retrieve a specific inquiry by its ID.
    """
    @swagger_auto_schema(
        operation_summary="Get Inquiry Details",
        operation_description="Retrieve detailed information about a specific inquiry, including user and customer service details.",
        responses={200: get_inquiry_response_schema, 404: "Inquiry Not Found"},
    )
    def get(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        serializer = GetInquirySerializer(inquiry)
        response_data = serializer.data
        response_data['user_role'] = request.user.role
        return JsonResponse(response_data, status=200)