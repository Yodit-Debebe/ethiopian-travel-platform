from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Destination

from io import BytesIO
from PIL import Image


class DestinationAPITests(APITestCase):

    def setUp(self):
        self.destinations = [
            Destination.objects.create(
                name="Abay",
                desc="Beautiful Blue Nile destination",
                price=700,
                img="pics/abay.jpg"
            ),
            Destination.objects.create(
                name="Hawassa",
                desc="Beautiful lakeside destination",
                price=750,
                img="pics/hawassa.jpg"
            ),
            Destination.objects.create(
                name="Axum",
                desc="Historic destination",
                price=650,
                img="pics/axum.jpg"
            ),
            Destination.objects.create(
                name="Fasilides Palaces",
                desc="Historic palace complex",
                price=600,
                img="pics/fasilides.jpg"
            ),
        ]

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

    def test_authenticated_user_can_create_destination(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        data = {
            "name": "Test Destination",
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
                name="Test Destination"
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
