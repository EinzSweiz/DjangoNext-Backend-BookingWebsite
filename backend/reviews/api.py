from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ReviewReportCreateSerializer, ReviewModelDynamicSerializer
from .models import Review, Property, ReviewReport
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from .swagger_usecases import paginated_reviews_schema, report_create_response_schema, report_create_schema, review_create_response_schema, review_create_schema

@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve Paginated Reviews",
    operation_description="Fetch paginated reviews for a specific property, excluding dismissed reports.",
    responses={200: paginated_reviews_schema, 500: "Internal Server Error"}
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_reviews_api(request, pk):
    """
    Retrieve paginated reviews for a specific property.
    """
    try:
        property_instance = get_object_or_404(Property, pk=pk)
        qs = Review.objects.filter(
            property=property_instance
        ).exclude(
            reports__status=ReviewReport.Status.DISMISSED
        ).order_by('-created_at')

        # Pagination parameters
        page_number = request.GET.get('page', 1)  # Default to page 1 if not provided
        page_size = request.GET.get('page_size', 5)  # Default page size

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


@swagger_auto_schema(
    method="post",
    operation_summary="Create a Review",
    operation_description="Submit a review for a specific property.",
    request_body=review_create_schema,
    responses={201: review_create_response_schema, 400: "Validation Error", 500: "Internal Server Error"}
)
@api_view(['POST'])
def create_reviews_api(request, pk):
    """
    Create a review for a specific property.
    """
    try:
        property_instance = get_object_or_404(Property, pk=pk)  # Retrieve the property instance
        data = request.data.copy()

        # Debug: Log incoming data
        print(f"Received data: {data}")

        serializer = ReviewModelDynamicSerializer(data=data, fields=['id', 'property', 'text', 'user'], context={'request': request})
        
        # Debug: Log serializer validation
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the review and pass property explicitly
        serializer.save(user=request.user, property=property_instance)
        
        return Response({'success': 'Review was created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error traceback to the console
        return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="post",
    operation_summary="Create a Review Report",
    operation_description="Submit a report for a specific review.",
    request_body=report_create_schema,
    responses={201: report_create_response_schema, 400: "Validation Error", 500: "Internal Server Error"}
)
@api_view(['POST'])
def report_create_api(request, pk):
    """
    Create a report for a specific review.
    """
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
