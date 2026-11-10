
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from travello.models import Destination
from bookings.models import Booking
from payments.models import Payment

from .models import Review


class ReviewAPITestCase(TestCase):

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
            desc="Destination for review testing",
            price=700,
            img="pics/test.jpg"
        )

        self.booking = Booking.objects.create(
            user=self.customer,
            destination=self.destination,
            travel_date=date.today() - timedelta(days=10),
            number_of_travelers=2,
            total_price=Decimal("1400.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        self.payment = Payment.objects.create(
            booking=self.booking,
            amount=self.booking.total_price,
            payment_method=Payment.PaymentMethod.TELEBIRR,
            status=Payment.PaymentStatus.SUCCESSFUL
        )

        self.client.force_authenticate(user=self.customer)

    def create_review(self, booking=None, status="PENDING"):

        if booking is None:
            booking = self.booking

        return Review.objects.create(
            booking=booking,
            user=booking.user,
            destination=booking.destination,
            rating=5,
            comment="Excellent destination!",
            status=status
        )

    def test_customer_can_create_review(self):

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 5,
                "comment": "Excellent destination!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["status"], "PENDING")

        self.assertEqual(Review.objects.count(), 1)

    def test_customer_cannot_review_unpaid_booking(self):

        self.payment.status = Payment.PaymentStatus.FAILED
        self.payment.save()

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 5,
                "comment": "Great trip!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_review_future_trip(self):

        self.booking.travel_date = date.today() + timedelta(days=10)
        self.booking.save()

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 5,
                "comment": "Great trip!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_review_pending_booking(self):

        self.booking.status = Booking.BookingStatus.PENDING
        self.booking.save()

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 5,
                "comment": "Great trip!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_review_another_customers_booking(self):

        booking = Booking.objects.create(
            user=self.another_customer,
            destination=self.destination,
            travel_date=date.today() - timedelta(days=5),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_method=Payment.PaymentMethod.CBE_BIRR,
            status=Payment.PaymentStatus.SUCCESSFUL
        )

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": booking.id,
                "rating": 5,
                "comment": "Great trip!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_create_duplicate_review(self):

        self.create_review()

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 4,
                "comment": "Another review!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_submit_invalid_rating(self):

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 6,
                "comment": "Great trip!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_submit_empty_comment(self):

        response = self.client.post(
            "/api/reviews/my/",
            {
                "booking": self.booking.id,
                "rating": 5,
                "comment": "   ",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_can_view_own_reviews(self):

        self.create_review()

        response = self.client.get("/api/reviews/my/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_customer_can_edit_own_review(self):

        review = self.create_review()

        response = self.client.patch(
            f"/api/reviews/my/{review.id}/",
            {
                "rating": 4,
                "comment": "Updated review!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        review.refresh_from_db()

        self.assertEqual(review.rating, 4)
        self.assertEqual(review.status, "PENDING")

    def test_customer_cannot_edit_another_customers_review(self):

        booking = Booking.objects.create(
            user=self.another_customer,
            destination=self.destination,
            travel_date=date.today() - timedelta(days=5),
            number_of_travelers=1,
            total_price=Decimal("700.00"),
            status=Booking.BookingStatus.CONFIRMED
        )

        review = self.create_review(booking=booking)

        response = self.client.patch(
            f"/api/reviews/my/{review.id}/",
            {"rating": 2},
            format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_customer_can_delete_own_review(self):

        review = self.create_review()

        response = self.client.delete(
            f"/api/reviews/my/{review.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Review.objects.filter(id=review.id).exists()
        )

    def test_public_users_only_see_approved_reviews(self):

        self.create_review()

        self.client.force_authenticate(user=None)

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_public_users_can_see_approved_reviews(self):

        self.create_review(
            status=Review.ModerationStatus.APPROVED
        )

        self.client.force_authenticate(user=None)

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_customer_cannot_access_admin_reviews(self):

        response = self.client.get("/api/reviews/admin/")

        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_all_reviews(self):

        self.create_review()

        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/reviews/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_approve_review(self):

        review = self.create_review()

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/reviews/admin/{review.id}/moderate/",
            {"status": "APPROVED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        review.refresh_from_db()

        self.assertEqual(
            review.status,
            Review.ModerationStatus.APPROVED
        )

    def test_admin_can_reject_review(self):

        review = self.create_review()

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/reviews/admin/{review.id}/moderate/",
            {"status": "REJECTED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        review.refresh_from_db()

        self.assertEqual(
            review.status,
            Review.ModerationStatus.REJECTED
        )

    def test_admin_cannot_moderate_with_invalid_status(self):

        review = self.create_review()

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/reviews/admin/{review.id}/moderate/",
            {"status": "PENDING"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_admin_cannot_moderate_review_twice(self):

        review = self.create_review(
            status=Review.ModerationStatus.APPROVED
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/reviews/admin/{review.id}/moderate/",
            {"status": "REJECTED"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)
