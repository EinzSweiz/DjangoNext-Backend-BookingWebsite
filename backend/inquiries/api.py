from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from .models import Inquiry
from useraccounts.models import User
from rest_framework.parsers import JSONParser
from django.http import Http404
from .serializers import CreateInquirySerializer, GetInquirySerializer, MessageSerializer, UpdateStatusSerializer, AssignInquirySerializer, CustomerServiceAgentSerializer


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
    

@api_view(['GET'])
def inquiries_view(request):
    if request.user.role == User.RoleChoises.ADMIN:
        inquiries = Inquiry.objects.all()
    elif request.user.role == User.RoleChoises.CUSTOMER_SERVICE:
        inquiries = Inquiry.objects.filter(customer_service=request.user, is_assigned_to_customer_service=True).select_related('user', 'customer_service')
    else:
        inquiries = Inquiry.objects.filter(user=request.user)

    inquiries_serializer = GetInquirySerializer(inquiries, many=True)
    return JsonResponse(inquiries_serializer.data, safe=False)

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
    inquiry.status = Inquiry.StatusChoice.IN_PROGRESS  # Optionally update the status
    inquiry.save()

    return JsonResponse({'success': 'Inquiry successfully assigned to agent'}, status=200)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def inquiry_queue(request):
    try:
        inquiry = Inquiry.objects.filter(is_assigned_to_customer_service=False)
        return JsonResponse({'success': 'recieved all unissigned unquiries'}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=400)

@api_view(['GET'])
def get_customer_service_agents(request):
    qs = User.objects.filter(role=User.RoleChoises.CUSTOMER_SERVICE)
    print("QuerySet:", qs)  # Log the QuerySet
    serializer = CustomerServiceAgentSerializer(qs, many=True)
    print("Serialized Data:", serializer.data)  # Log the serialized data
    return JsonResponse(serializer.data, safe=False)

@api_view(['PUT'])
def update_inquiry_status(request, pk):
    try:
        inquiry = Inquiry.objects.get(pk=pk)
        data = JSONParser().parse(request)
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
        inquiry = Inquiry.objects.get(pk=pk)
        serializer = GetInquirySerializer(inquiry)
        return JsonResponse(serializer.data, status=200)
    except Inquiry.DoesNotExist:
        return JsonResponse({"error": "Inquiry not found"}, status=404)
