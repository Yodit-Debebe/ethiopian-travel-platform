
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from travello.models import Destination
from bookings.models import Booking
from .models import Payment


class PaymentAPITestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.customer = User.objects.create_user(
            username="customer1",
            password="testpassword123"
        )

        self.another_customer = User.objects.create_user(
            username="customer2",
            password="testpassword123"
        )

        self.admin = User.objects.create_user(
            username="admin1",
            password="adminpassword123",
            is_staff=True
        )

        self.destination = Destination.objects.create(
            name="Test Destination",
            desc="A destination for testing",
            price=700,
            img="pics/test.jpg"
        )

        self.booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=30),
            number_of_travelers=2,
            total_price=Decimal("1400.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        self.client.force_authenticate(user=self.customer)

    def create_payment(self, booking=None, status="PENDING"):

        if booking is None:
            booking = self.booking

        return Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_method=Payment.PaymentMethod.TELEBIRR,
            status=status
        )

    def test_customer_can_create_payment(self):

        response = self.client.post(
            "/api/payments/",
            {
                "booking": self.booking.id,
                "payment_method": "TELEBIRR",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"], "1400.00")
        self.assertEqual(response.data["status"], "PENDING")

        self.assertEqual(Payment.objects.count(), 1)

    def test_payment_amount_is_calculated_by_backend(self):

        response = self.client.post(
            "/api/payments/",
            {
                "booking": self.booking.id,
                "payment_method": "CBE_BIRR",
                "amount": "1.00",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"], "1400.00")

    def test_customer_cannot_pay_for_unconfirmed_booking(self):

        booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=40),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.PENDING
        )

        response = self.client.post(
            "/api/payments/",
            {
                "booking": booking.id,
                "payment_method": "TELEBIRR",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Payment.objects.count(), 0)

    def test_customer_cannot_pay_for_another_customers_booking(self):

        booking = Booking.objects.create(
            user=self.another_customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=40),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        response = self.client.post(
            "/api/payments/",
            {
                "booking": booking.id,
                "payment_method": "TELEBIRR",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_create_duplicate_active_payment(self):

        self.create_payment()

        response = self.client.post(
            "/api/payments/",
            {
                "booking": self.booking.id,
                "payment_method": "CBE_BIRR",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Payment.objects.count(), 1)

    def test_customer_can_view_own_payments(self):

        self.create_payment()

        response = self.client.get("/api/payments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_customer_cannot_view_another_customers_payments(self):

        booking = Booking.objects.create(
            user=self.another_customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=40),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        self.create_payment(booking=booking)

        response = self.client.get("/api/payments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_access_payments(self):

        self.client.force_authenticate(user=None)

        response = self.client.get("/api/payments/")

        self.assertEqual(response.status_code, 401)

    def test_customer_can_simulate_successful_payment(self):

        payment = self.create_payment()

        response = self.client.post(
            f"/api/payments/{payment.id}/simulate/",
            {"result": "SUCCESSFUL"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.SUCCESSFUL
        )

    def test_customer_can_simulate_failed_payment(self):

        payment = self.create_payment()

        response = self.client.post(
            f"/api/payments/{payment.id}/simulate/",
            {"result": "FAILED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.FAILED
        )

    def test_customer_cannot_simulate_invalid_result(self):

        payment = self.create_payment()

        response = self.client.post(
            f"/api/payments/{payment.id}/simulate/",
            {"result": "REFUNDED"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.PENDING
        )

    def test_customer_cannot_simulate_another_customers_payment(self):

        booking = Booking.objects.create(
            user=self.another_customer,
            destination=self.destination,
            travel_date=date.today() + timedelta(days=40),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        payment = self.create_payment(booking=booking)

        response = self.client.post(
            f"/api/payments/{payment.id}/simulate/",
            {"result": "SUCCESSFUL"},
            format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_customer_cannot_process_completed_payment(self):

        payment = self.create_payment(
            status=Payment.PaymentStatus.SUCCESSFUL
        )

        response = self.client.post(
            f"/api/payments/{payment.id}/simulate/",
            {"result": "FAILED"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_access_admin_payment_list(self):

        response = self.client.get("/api/payments/admin/")

        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_all_payments(self):

        self.create_payment()

        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/payments/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_refund_successful_payment(self):

        payment = self.create_payment(
            status=Payment.PaymentStatus.SUCCESSFUL
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/payments/admin/{payment.id}/refund/"
        )

        self.assertEqual(response.status_code, 200)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.REFUNDED
        )

    def test_admin_cannot_refund_pending_payment(self):

        payment = self.create_payment()

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/payments/admin/{payment.id}/refund/"
        )

        self.assertEqual(response.status_code, 400)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.PENDING
        )

    def test_admin_cannot_refund_failed_payment(self):

        payment = self.create_payment(
            status=Payment.PaymentStatus.FAILED
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/payments/admin/{payment.id}/refund/"
        )

        self.assertEqual(response.status_code, 400)

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.PaymentStatus.FAILED
        )
