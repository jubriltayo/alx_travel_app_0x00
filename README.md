## Project Overview

This project implements a Django-based travel application, featuring models for `Listing`, `Booking`, and `Review`. It includes serializers to format data for API responses and a management command to populate the database with sample data.

## Objective

- Define the database models for `Listing`, `Booking`, and `Review`.
- Set up serializers for the `Listing` and `Booking` models.
- Implement a management command to seed the database with sample data.

## Features

- **Models**:
  - `Listing`: Represents property listings with details like price, description, and location.
  - `Booking`: Represents bookings for properties, including start and end dates, total price, and status.
  - `Review`: Represents user reviews with ratings and comments for listings.
  
- **Serializers**:
  - `ListingSerializer`: Converts `Listing` model instances into JSON data.
  - `BookingSerializer`: Converts `Booking` model instances into JSON data.

- **Seeder**: 
  - A management command `seed.py` to populate the database with sample listings, bookings, and reviews.

## Installation and Setup

1. Clone or download the repository.

2. Set up a virtual environment:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate # On Mac or gitbash, use source .venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```

## Database Models

### `Listing`
Represents a property listing in the app.
- `listing_id` (UUIDField): Unique identifier for the listing.
- `name` (CharField): Name of the property.
- `description` (TextField): Detailed description of the property.
- `location` (CharField): Location of the property.
- `price_per_night` (DecimalField): Price per night for booking.
- `created_at` (DateTimeField): Date and time when the listing was created.
- `updated_at` (DateTimeField): Date and time when the listing was last updated.

### `Booking`
Represents a booking made for a property.
- `booking_id` (UUIDField): Unique identifier for the booking.
- `listing` (ForeignKey to `Listing`): The listing that was booked.
- `start_date` (DateField): Start date of the booking.
- `end_date` (DateField): End date of the booking.
- `total_price` (DecimalField): Total price for the booking.
- `status` (CharField): Booking status (`pending`, `confirmed`, `cancelled`).
- `created_at` (DateTimeField): Date and time when the booking was created.

### `Review`
Represents a review made by a user for a property.
- `review_id` (UUIDField): Unique identifier for the review.
- `listing` (ForeignKey to `Listing`): The listing that the review is for.
- `rating` (IntegerField): Rating given to the listing (1-5 stars).
- `comment` (TextField): Review comment.
- `created_at` (DateTimeField): Date and time when the review was created.

## Serializers

### `ListingSerializer`
Serializes data for the `Listing` model.
```python
class ListingSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['listing_id', 'created_at', 'updated_at']
```

### `BookingSerializer`
Serializes data for the `Booking` model. It includes custom validation to ensure the `start_date` is earlier than the `end_date`.
```python
class BookingSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['booking_id', 'created_at']

    def validate(self, data):
        """ Custom validation to ensure start_date < end_date """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Start date must be before end date.")
        return data
```

## Seeder

A management command is available to populate the database with sample data for `Listing`, `Booking`, and `Review` models.

### How to Run the Seeder
```bash
python manage.py seed 10
```

This command will create random `Listing`, `Booking`, and `Review` entries in the database.

## Notes

- Ensure that your database has been properly configured and migrated before running the seed command.
- The `UUIDField` is used for `listing_id` and `booking_id` to generate globally unique identifiers.