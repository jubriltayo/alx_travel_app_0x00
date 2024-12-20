from rest_framework import serializers
from listings.models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.

    Handles the serialization and deserialization of Listing instances,
    enabling conversion between Python objects and JSON representations.
    Maps the following fields to JSON:
        - listing_id: UUID, unique identifier for the listing (read-only).
        - name: Name of the property, max_length=50.
        - description: Text field for detailed property description.
        - location: Location/address of the property, max_length=50.
        - price_per_night: Decimal value representing nightly rate.
        - created_at: Timestamp when the listing was created (read-only).
        - updated_at: Timestamp when the listing was last updated (read-only).
    """
    class Meta:
        model = Listing
        fields = [
            'listing_id',
            'name',
            'description',
            'location',
            'price_per_night',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['listing_id','created_at', 'updated_at']



class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.

    Handles serialization and deserialization of Booking instances
    and includes validation logic to enforce data integrity.
    Maps the following fields to JSON:
        - booking_id: UUID, unique identifier for the booking (read-only).
        - listing: ForeignKey referencing the associated Listing (PrimaryKeyRelatedField).
        - start_date: Date when the booking begins.
        - end_date: Date when the booking ends.
        - total_price: Decimal value representing the total booking cost.
        - status: String field representing the booking status, with choices such as 'Pending', 'Confirmed', 'Cancelled'.
        - created_at: Timestamp when the booking was created (read-only).

    Validation:
        - Ensures the start_date is earlier than the end_date, raising a ValidationError otherwise.
    """

    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'listing',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'created_at',
        ]
        read_only_fields = ['booking_id','created_at']

    def validate(self, data):
        """
        Custom validation method.

        Ensures that the start_date is earlier than the end_date.
        Raises:
            serializers.ValidationError: If start_date is not before end_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Start date must be before end date.")
        return data