
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from travello.models import Destination
from .models import Booking


class BookingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.customer = User.objects.create_user(
            username="customer1",
            password="testpassword123"
        )

        self.destination = Destination.objects.create(
            name="Test Destination",
            desc="A destination for testing",
            price=700,
            img="pics/test.jpg"
        )

        self.client.force_authenticate(user=self.customer)

    def test_customer_can_create_booking(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "destination": self.destination.id,
                "travel_date": date.today() + timedelta(days=30),
                "number_of_travelers": 2,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_price"], "1400.00")
        self.assertEqual(response.data["status"], "PENDING")

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(
            Booking.objects.first().user,
            self.customer
        )
    
    def test_customer_cannot_book_past_date(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "destination": self.destination.id,
                "travel_date": date.today() - timedelta(days=1),
                "number_of_travelers": 2,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("travel_date", response.data)

        self.assertEqual(Booking.objects.count(), 0)

    
    def test_customer_cannot_book_with_zero_travelers(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "destination": self.destination.id,
                "travel_date": date.today() + timedelta(days=30),
                "number_of_travelers": 0,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("number_of_travelers", response.data)

        self.assertEqual(Booking.objects.count(), 0)

    
    def test_customer_can_only_see_own_bookings(self):
        another_customer = User.objects.create_user(
            username="customer2",
            password="testpassword123"
        )

        Booking.objects.create(
            user=another_customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    
    def test_unauthenticated_user_cannot_access_bookings(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, 401)

    
    def test_customer_cannot_access_admin_booking_list(self):
        response = self.client.get("/api/bookings/admin/")

        self.assertEqual(response.status_code, 403)

    
    def test_admin_can_access_all_bookings(self):
        admin = User.objects.create_user(
            username="admin1",
            password="adminpassword123",
            is_staff=True
        )

        self.client.force_authenticate(user=admin)

        response = self.client.get("/api/bookings/admin/")

        self.assertEqual(response.status_code, 200)

    
    def test_admin_can_confirm_pending_booking(self):
        admin = User.objects.create_user(
            username="admin2",
            password="adminpassword123",
            is_staff=True
        )

        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/bookings/admin/{booking.id}/manage/",
            {"status": "CONFIRMED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CONFIRMED
        )

    
    def test_admin_can_cancel_pending_booking(self):
        admin = User.objects.create_user(
            username="admin3",
            password="adminpassword123",
            is_staff=True
        )

        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/bookings/admin/{booking.id}/manage/",
            {"status": "CANCELLED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CANCELLED
        )

    
    def test_admin_cannot_set_invalid_booking_status(self):
        admin = User.objects.create_user(
            username="admin4",
            password="adminpassword123",
            is_staff=True
        )

        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/bookings/admin/{booking.id}/manage/",
            {"status": "COMPLETED"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.PENDING
        )

    
    def test_admin_cannot_modify_already_confirmed_booking(self):
        admin = User.objects.create_user(
            username="admin5",
            password="adminpassword123",
            is_staff=True
        )

        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/bookings/admin/{booking.id}/manage/",
            {"status": "CANCELLED"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CONFIRMED
        )

    
    def test_customer_cannot_cancel_confirmed_booking(self):
        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        response = self.client.post(
            f"/api/bookings/{booking.id}/cancel/"
        )

        self.assertEqual(response.status_code, 400)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CONFIRMED
        )

    
    def test_customer_cannot_cancel_another_customers_booking(self):
        another_customer = User.objects.create_user(
            username="customer3",
            password="testpassword123"
        )

        booking = Booking.objects.create(
            user=another_customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        response = self.client.post(
            f"/api/bookings/{booking.id}/cancel/"
        )

        self.assertEqual(response.status_code, 404)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.PENDING
        )

    def test_customer_cannot_create_booking_for_invalid_destination(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "destination": 99999,
                "travel_date": date.today() + timedelta(days=30),
                "number_of_travelers": 2,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Booking.objects.count(), 0)

    def test_admin_cannot_access_manage_endpoint_as_customer(self):
        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00")
        )

        response = self.client.patch(
            f"/api/bookings/admin/{booking.id}/manage/",
            {"status": "CONFIRMED"},
            format="json"
        )

        self.assertEqual(response.status_code, 403)

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.PENDING
        )

    def test_admin_cannot_manage_nonexistent_booking(self):
        admin = User.objects.create_user(
            username="admin6",
            password="adminpassword123",
            is_staff=True
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            "/api/bookings/admin/99999/manage/",
            {"status": "CONFIRMED"},
            format="json"
        )

        self.assertEqual(response.status_code, 404)





