from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ReviewViewSerializer, ReviewCreateSerializer
from .models import Review, Property

@api_view(['GET'])
def get_reviews_api(request, pk):
    """
    Retrieve all reviews for a specific property.
    """
    try:
        property = get_object_or_404(Property, pk=pk)
        qs = Review.objects.filter(property=property)
        serializer = ReviewViewSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_reviews_api(request, pk):
    """
    Create a review for a specific property.
    """
    try:
        property_instance = get_object_or_404(Property, pk=pk)  # Retrieve the property instance
        data = request.data.copy()
        serializer = ReviewCreateSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(user=request.user, property=property_instance)  # Pass property instance explicitly
            return Response({'success': 'Review was created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
