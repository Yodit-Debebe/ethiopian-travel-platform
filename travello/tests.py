
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO

from PIL import Image

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from bookings.models import Booking
from reviews.models import Review

from .models import Destination


class DestinationAPITests(APITestCase):

    def setUp(self):
        self.destinations = [
            Destination.objects.create(
                name="Abay",
                desc="Beautiful Blue Nile destination",
                price=700,
                img="pics/abay.jpg",
                category=Destination.Category.NATURAL
            ),
            Destination.objects.create(
                name="Hawassa",
                desc="Beautiful lakeside destination",
                price=750,
                img="pics/hawassa.jpg",
                category=Destination.Category.LAKE
            ),
            Destination.objects.create(
                name="Axum",
                desc="Historic destination",
                price=650,
                img="pics/axum.jpg",
                category=Destination.Category.HISTORICAL
            ),
            Destination.objects.create(
                name="Fasilides Palaces",
                desc="Historic palace complex",
                price=600,
                img="pics/fasilides.jpg",
                category=Destination.Category.HISTORICAL
            ),
        ]

    def create_approved_review(self, destination, rating):
        user = User.objects.create_user(
            username=f"reviewer_{destination.id}_{rating}",
            password="testpassword123"
        )

        booking = Booking.objects.create(
            user=user,
            destination=destination,
            travel_date=date.today() - timedelta(days=30),
            number_of_travelers=1,
            total_price=Decimal(str(destination.price)),
            status=Booking.BookingStatus.CONFIRMED
        )

        return Review.objects.create(
            booking=booking,
            user=user,
            destination=destination,
            rating=rating,
            comment="Excellent destination!",
            status=Review.ModerationStatus.APPROVED
        )

    # EXISTING DESTINATION API TESTS

    def test_destination_list(self):
        url = reverse("destination-list-api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_destination_detail(self):
        destination = self.destinations[0]

        url = reverse(
            "destination-detail-api",
            kwargs={"pk": destination.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Abay")

    def test_search_destinations(self):
        url = reverse("destination-list-api")
        response = self.client.get(url, {"search": "Hawassa"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_min_price_filter(self):
        url = reverse("destination-list-api")
        response = self.client.get(url, {"min_price": 650})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_price_ordering(self):
        url = reverse("destination-list-api")
        response = self.client.get(url, {"ordering": "-price"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["price"], 750)

    def test_pagination(self):
        url = reverse("destination-list-api")
        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    # CATEGORY FILTERING TESTS

    def test_category_filter(self):
        url = reverse("destination-list-api")

        response = self.client.get(
            url,
            {"category": "HISTORICAL"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        names = [
            item["name"]
            for item in response.data["results"]
        ]

        self.assertIn("Axum", names)
        self.assertIn("Fasilides Palaces", names)

    def test_invalid_category_returns_bad_request(self):
        url = reverse("destination-list-api")

        response = self.client.get(
            url,
            {"category": "INVALID"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_category_and_price_filters_together(self):
        url = reverse("destination-list-api")

        response = self.client.get(
            url,
            {
                "category": "HISTORICAL",
                "min_price": 650
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Axum"
        )

    # RATING FILTERING TESTS

    def test_minimum_rating_filter(self):
        abay = self.destinations[0]
        hawassa = self.destinations[1]
        axum = self.destinations[2]

        self.create_approved_review(abay, 5)
        self.create_approved_review(hawassa, 3)
        self.create_approved_review(axum, 4)

        url = reverse("destination-list-api")

        response = self.client.get(
            url,
            {"min_rating": 4}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        names = {
            item["name"]
            for item in response.data["results"]
        }

        self.assertEqual(names, {"Abay", "Axum"})

    def test_invalid_minimum_rating_returns_bad_request(self):
        url = reverse("destination-list-api")

        invalid_values = ["abc", "0", "6"]

        for value in invalid_values:
            with self.subTest(min_rating=value):
                response = self.client.get(
                    url,
                    {"min_rating": value}
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST
                )

    def test_rating_ordering(self):
        abay = self.destinations[0]
        hawassa = self.destinations[1]
        axum = self.destinations[2]

        self.create_approved_review(abay, 5)
        self.create_approved_review(hawassa, 3)
        self.create_approved_review(axum, 4)

        url = reverse("destination-list-api")

        response = self.client.get(
            url,
            {"ordering": "-average_rating"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        self.assertEqual(results[0]["name"], "Abay")
        self.assertEqual(results[1]["name"], "Axum")
        self.assertEqual(results[2]["name"], "Hawassa")

        self.assertEqual(results[0]["average_rating"], 5)
        self.assertEqual(results[1]["average_rating"], 4)
        self.assertEqual(results[2]["average_rating"], 3)

    def test_destination_response_includes_rating_information(self):
        url = reverse("destination-list-api")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        destination = response.data["results"][0]

        self.assertIn("category", destination)
        self.assertIn("average_rating", destination)
        self.assertIn("review_count", destination)


class DestinationCreationAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="adminuser",
            password="testpassword123",
            is_staff=True
        )

        self.token = Token.objects.create(user=self.user)

        self.regular_user = User.objects.create_user(
            username="regularuser",
            password="testpassword123"
        )

        self.regular_token = Token.objects.create(
            user=self.regular_user
        )

        self.url = reverse("destination-create-api")

        self.destination = Destination.objects.create(
            name="Test Destination",
            desc="Original description",
            price=500,
            img="pics/test.jpg"
        )

        self.manage_url = reverse(
            "destination-manage-api",
            kwargs={"pk": self.destination.id}
        )

    def get_test_image(self):
        image_buffer = BytesIO()

        image = Image.new(
            "RGB",
            (100, 100),
            color="blue"
        )

        image.save(image_buffer, format="JPEG")
        image_buffer.seek(0)

        return SimpleUploadedFile(
            name="test_destination.jpg",
            content=image_buffer.getvalue(),
            content_type="image/jpeg"
        )

    # CREATE TESTS

    def test_authenticated_user_can_create_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        data = {
            "name": "New Destination",
            "desc": "A destination created through automated testing",
            "price": 500,
            "img": self.get_test_image()
        }

        response = self.client.post(
            self.url,
            data,
            format="multipart"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Destination.objects.filter(
                name="New Destination"
            ).exists()
        )

    def test_unauthenticated_user_cannot_create_destination(self):
        data = {
            "name": "Unauthorized Destination",
            "desc": "This should not be created",
            "price": 500,
            "img": self.get_test_image()
        }

        response = self.client.post(
            self.url,
            data,
            format="multipart"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertFalse(
            Destination.objects.filter(
                name="Unauthorized Destination"
            ).exists()
        )

    def test_created_destination_has_correct_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        data = {
            "name": "Lalibela",
            "desc": "Historic rock-hewn churches",
            "price": 800,
            "img": self.get_test_image()
        }

        response = self.client.post(
            self.url,
            data,
            format="multipart"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        destination = Destination.objects.get(
            name="Lalibela"
        )

        self.assertEqual(destination.price, 800)
        self.assertEqual(
            destination.desc,
            "Historic rock-hewn churches"
        )

    def test_regular_user_cannot_create_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.regular_token.key}"
        )

        data = {
            "name": "Unauthorized Destination",
            "desc": "Regular users cannot create destinations",
            "price": 500,
            "img": self.get_test_image()
        }

        response = self.client.post(
            self.url,
            data,
            format="multipart"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertFalse(
            Destination.objects.filter(
                name="Unauthorized Destination"
            ).exists()
        )

    # UPDATE TESTS

    def test_admin_can_update_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        data = {
            "name": "Updated Destination",
            "desc": "Updated description",
            "price": 900,
        }

        response = self.client.patch(
            self.manage_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.destination.refresh_from_db()

        self.assertEqual(
            self.destination.name,
            "Updated Destination"
        )

        self.assertEqual(self.destination.price, 900)

    def test_regular_user_cannot_update_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.regular_token.key}"
        )

        response = self.client.patch(
            self.manage_url,
            {"name": "Unauthorized Update"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.destination.refresh_from_db()

        self.assertEqual(
            self.destination.name,
            "Test Destination"
        )

    # DELETE TESTS

    def test_admin_can_delete_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.delete(self.manage_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Destination.objects.filter(
                id=self.destination.id
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_destination(self):
        response = self.client.delete(self.manage_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertTrue(
            Destination.objects.filter(
                id=self.destination.id
            ).exists()
        )
