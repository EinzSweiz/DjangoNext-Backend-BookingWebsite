from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .models import Inquiry
from useraccounts.models import User
from rest_framework.parsers import JSONParser
from django.http import Http404
from .serializers import CreateInquirySerializer, GetInquirySerializer, MessageSerializer


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

def handle_get_request(inquiry):
    serializer = GetInquirySerializer(inquiry)
    return JsonResponse(serializer.data, status=200)

def handle_put_request(request, inquiry):
    data = JSONParser().parse(request)
    serializer = GetInquirySerializer(inquiry, data=data, partial=False)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)

def handle_post_request(request, inquiry):
    data = JSONParser().parse(request)
    message_data = {'inquiry': inquiry.id, 'sender': data.get('sender'), 'message': data.get('message')}
    message_serializer = MessageSerializer(data=message_data)
    if message_serializer.is_valid():
        message_serializer.save()
        return JsonResponse({'message': 'Message added successfully'}, status=201)
    return JsonResponse(message_serializer.errors, status=400)

@api_view(['GET', 'PUT', 'POST'])
def inquiry_detail_api(request, pk):
    try:
        inquiry = Inquiry.objects.get(pk=pk)
        if request.method == 'GET':
            return handle_get_request(inquiry)
        elif request.method == 'PUT':
            return handle_put_request(request, inquiry)
        elif request.method == 'POST':
            return handle_post_request(request, inquiry)
    except Inquiry.DoesNotExist:
        raise Http404("Inquiry not found")
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)
