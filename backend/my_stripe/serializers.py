from rest_framework import serializers

class BookingSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    number_of_nights = serializers.IntegerField()
    guests = serializers.IntegerField()
    has_paid = serializers.BooleanField(required=False, default=False)  # Add this field