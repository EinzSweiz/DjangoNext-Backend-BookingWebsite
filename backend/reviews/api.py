from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from .serializers import ReviewReportCreateSerializer, ReviewModelDynamicSerializer
from .models import Review, Property, ReviewReport
from drf_yasg.utils import swagger_auto_schema
from .swagger_usecases import (
    paginated_reviews_schema,
    report_create_response_schema,
    report_create_schema,
    review_create_response_schema,
    review_create_schema
)


class GetReviewsAPIView(APIView):
    """
    Retrieve paginated reviews for a specific property.
    """
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        method='get',
        operation_summary="Retrieve Paginated Reviews",
        operation_description="Fetch paginated reviews for a specific property, excluding dismissed reports.",
        responses={200: paginated_reviews_schema, 500: "Internal Server Error"}
    )
    def get(self, request, pk):
        try:
            property_instance = get_object_or_404(Property, pk=pk)
            qs = Review.objects.filter(
                property=property_instance
            ).exclude(
                reports__status=ReviewReport.Status.DISMISSED
            ).order_by('-created_at')

            # Pagination parameters
            page_number = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 5)

            paginator = Paginator(qs, page_size)
            page = paginator.get_page(page_number)

            # Serialize the paginated data
            serializer = ReviewModelDynamicSerializer(page.object_list, fields=['id', 'user', 'text', 'created_at'], many=True)

            # Return paginated response
            return Response({
                'total_pages': paginator.num_pages,
                'current_page': page.number,
                'total_reviews': paginator.count,
                'reviews': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateReviewAPIView(APIView):
    """
    Create a review for a specific property.
    """
    @swagger_auto_schema(
        method='post',
        operation_summary="Create a Review",
        operation_description="Submit a review for a specific property.",
        request_body=review_create_schema,
        responses={201: review_create_response_schema, 400: "Validation Error", 500: "Internal Server Error"}
    )
    def post(self, request, pk):
        try:
            property_instance = get_object_or_404(Property, pk=pk)
            data = request.data.copy()

            # Debugging: Log incoming data
            serializer = ReviewModelDynamicSerializer(data=data, fields=['id', 'property', 'text', 'user'], context={'request': request})
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the review and pass property explicitly
            serializer.save(user=request.user, property=property_instance)
            
            return Response({'success': 'Review was created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()  # Log full error traceback
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateReviewReportAPIView(APIView):
    """
    Submit a report for a specific review.
    """
    @swagger_auto_schema(
        method='post',
        operation_summary="Create a Review Report",
        operation_description="Submit a report for a specific review.",
        request_body=report_create_schema,
        responses={201: report_create_response_schema, 400: "Validation Error", 500: "Internal Server Error"}
    )
    def post(self, request, pk):
        try:
            # Retrieve the review object
            review = get_object_or_404(Review, pk=pk)

            # Use the serializer
            serializer = ReviewReportCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                # Save the report and manually associate the review and user
                serializer.save(review=review, reported_by=request.user)
                return Response({'success': 'Report was created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            traceback.print_exc()  # Log the error for debugging
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
