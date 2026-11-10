
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from travello.models import Destination
from .models import Wishlist


class WishlistAPITests(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password="StrongPassword123"
        )

        self.user2 = User.objects.create_user(
            username="customer2",
            email="customer2@example.com",
            password="StrongPassword123"
        )

        self.destination1 = Destination.objects.create(
            name="Abay",
            desc="Beautiful Blue Nile destination",
            price=700,
            img="pics/abay.jpg"
        )

        self.destination2 = Destination.objects.create(
            name="Hawassa",
            desc="Beautiful lakeside destination",
            price=750,
            img="pics/hawassa.jpg"
        )

        self.list_url = reverse("wishlist-list-create")

        self.client.force_authenticate(user=self.user1)

    def test_customer_can_add_destination(self):

        response = self.client.post(
            self.list_url,
            {"destination": self.destination1.id}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Wishlist.objects.count(),
            1
        )

        self.assertEqual(
            Wishlist.objects.first().user,
            self.user1
        )

    def test_customer_can_view_own_wishlist(self):

        Wishlist.objects.create(
            user=self.user1,
            destination=self.destination1
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )
    def test_customer_cannot_view_another_users_wishlist(self):

        Wishlist.objects.create(
            user=self.user2,
            destination=self.destination2
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            0
        )
    def test_customer_cannot_add_same_destination_twice(self):

        Wishlist.objects.create(
            user=self.user1,
            destination=self.destination1
        )

        response = self.client.post(
            self.list_url,
            {"destination": self.destination1.id}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Wishlist.objects.filter(user=self.user1).count(),
            1
        )

    def test_customer_can_add_multiple_destinations(self):

        response1 = self.client.post(
            self.list_url,
            {"destination": self.destination1.id}
        )

        response2 = self.client.post(
            self.list_url,
            {"destination": self.destination2.id}
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Wishlist.objects.filter(user=self.user1).count(),
            2
        )

    def test_customer_can_remove_own_wishlist_item(self):

        item = Wishlist.objects.create(
            user=self.user1,
            destination=self.destination1
        )

        response = self.client.delete(
            reverse("wishlist-delete", kwargs={"pk": item.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Wishlist.objects.filter(id=item.id).exists()
        )

    def test_customer_cannot_remove_another_users_item(self):

        item = Wishlist.objects.create(
            user=self.user2,
            destination=self.destination2
        )

        response = self.client.delete(
            reverse("wishlist-delete", kwargs={"pk": item.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertTrue(
            Wishlist.objects.filter(id=item.id).exists()
        )

    def test_unauthenticated_customer_cannot_access_wishlist(self):

        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_customer_cannot_add_nonexistent_destination(self):

        response = self.client.post(
            self.list_url,
            {"destination": 999999}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
