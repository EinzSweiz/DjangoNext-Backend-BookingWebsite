from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .models import Inquiry
from useraccounts.models import User
from rest_framework.parsers import JSONParser
from django.http import Http404
from .serializers import CreateInquirySerializer, GetInquirySerializer, MessageSerializer, UpdateStatusSerializer


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
    if request.user.role == User.RoleChoises.CUSTOMER_SERVICE:
        inquiries = Inquiry.objects.all()
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
