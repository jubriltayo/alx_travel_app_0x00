from django.db import models
import uuid


STATUS = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
)

RATING = (
    ( 1, '★☆☆☆☆'),
    ( 2, '★★☆☆☆'),
    ( 3, '★★★☆☆'),
    ( 4, '★★★★☆'),
    ( 5, '★★★★★'),
)


class Listing(models.Model):
    """
    Represents a property listing available for booking.

    Fields:
        - listing_id (UUIDField): The unique identifier for the listing, auto-generated as a UUID.
        - name (CharField): The name of the property (e.g., "Cozy Apartment"), max_length=50.
        - description (TextField): A detailed description of the property.
        - location (CharField): The address or general location of the property, max_length=50.
        - price_per_night (DecimalField): The nightly rental price, allowing up to 7 digits with 2 decimal places.
        - created_at (DateTimeField): The timestamp when the listing was created (automatically set).
        - updated_at (DateTimeField): The timestamp when the listing was last updated (automatically updated).

    Meta:
        - ordering: Orders listings by the `created_at` field in descending order.
        - verbose_name: Human-readable name for the model ("Listing").
        - verbose_name_plural: Human-readable plural name for the model ("Listings").

    Methods:
        - __str__: Returns the name of the listing for easy representation in Django admin and other contexts.
    """

    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(blank=False)
    location = models.CharField(max_length=50, null=False, blank=False)
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def __str__(self):
        return self.name
    



class Booking(models.Model):
    """
    Represents a reservation made for a specific listing.

    Fields:
        - booking_id (UUIDField): The unique identifier for the booking, auto-generated as a UUID.
        - listing (ForeignKey): References the associated `Listing` (nullable; cascades as SET_NULL on deletion).
        - start_date (DateField): The date when the booking starts.
        - end_date (DateField): The date when the booking ends.
        - total_price (DecimalField): The total cost of the booking, allowing up to 10 digits with 2 decimal places.
        - status (CharField): The current status of the booking, with choices like "Pending", "Confirmed", and "Cancelled".
        - created_at (DateTimeField): The timestamp when the booking was created (automatically set).

    Meta:
        - ordering: Orders bookings by the `created_at` field in descending order.
        - verbose_name: Human-readable name for the model ("Booking").
        - verbose_name_plural: Human-readable plural name for the model ("Bookings").

    Methods:
        - __str__: Returns a string representation of the booking, including its ID and associated listing.
    """
    
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS, max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking {self.booking_id} ({self.listing})"

    

class Review(models.Model):
    """
    Represents a customer review for a specific listing.

    Fields:
        - review_id (UUIDField): The unique identifier for the review, auto-generated as a UUID.
        - listing (ForeignKey): References the associated `Listing` (nullable; cascades as SET_NULL on deletion).
        - rating (IntegerField): The rating provided by the customer, with choices from 1 to 5 stars.
        - comment (TextField): The textual feedback provided by the customer.
        - created_at (DateTimeField): The timestamp when the review was created (automatically set).

    Meta:
        - ordering: Orders reviews by the `created_at` field in descending order.
        - verbose_name: Human-readable name for the model ("Review").
        - verbose_name_plural: Human-readable plural name for the model ("Reviews").

    Methods:
        - __str__: Returns a string representation of the review, including its ID and rating.
    """

    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, related_name="reviews")
    rating = models.IntegerField(choices=RATING)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review {self.review_id} - {self.rating}★"
