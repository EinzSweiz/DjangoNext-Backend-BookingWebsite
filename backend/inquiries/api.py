from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from useraccounts.models import User
from .serializers import CreateInquirySerializer


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

