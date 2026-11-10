
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q

from travello.models import Destination

from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import DestinationSerializer


# Template Views

def home(request):
    destinations = Destination.objects.all()
    return render(request, 'home.html', {'destinations': destinations})


def welcome_page(request):
    return render(request, 'welcome.html')


@login_required(login_url='login')
def payment(request, id):
    destination = get_object_or_404(Destination, pk=id)

    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        method = request.POST.get('method')

        return render(request, 'payment_success.html', {
            'destination': destination,
            'name': name,
            'email': email,
            'method': method,
        })

    return render(request, 'payment.html', {'destination': destination})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in all fields.")
            return render(request, "contact.html")

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('contact')

    return render(request, "contact.html")


# API Pagination

class DestinationPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 6


# Destination List API

class DestinationListAPIView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = DestinationSerializer
    pagination_class = DestinationPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["name", "desc"]

    ordering_fields = [
        "name",
        "price",
        "id",
        "average_rating",
    ]

    ordering = ["id"]

    def get_queryset(self):

        queryset = Destination.objects.annotate(
            average_rating=Avg(
                "reviews__rating",
                filter=Q(reviews__status="APPROVED")
            ),
            review_count=Count(
                "reviews",
                filter=Q(reviews__status="APPROVED"),
                distinct=True
            )
        )

        # Price filtering

        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        try:
            min_price = int(min_price) if min_price is not None else None
            max_price = int(max_price) if max_price is not None else None
        except ValueError:
            raise ValidationError({
                "price": "min_price and max_price must be whole numbers."
            })

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValidationError({
                    "price": "min_price cannot be greater than max_price."
                })

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        # Category filtering

        category = self.request.query_params.get("category")

        if category:
            category = category.upper()

            valid_categories = Destination.Category.values

            if category not in valid_categories:
                raise ValidationError({
                    "category": (
                        f"Invalid category. Choose from: "
                        f"{', '.join(valid_categories)}"
                    )
                })

            queryset = queryset.filter(category=category)

        # Minimum rating filtering

        min_rating = self.request.query_params.get("min_rating")

        if min_rating is not None:
            try:
                min_rating = float(min_rating)
            except ValueError:
                raise ValidationError({
                    "min_rating": "min_rating must be a number."
                })

            if not 1 <= min_rating <= 5:
                raise ValidationError({
                    "min_rating": "min_rating must be between 1 and 5."
                })

            queryset = queryset.filter(
                average_rating__gte=min_rating
            )

        return queryset.order_by("id")


# Destination Detail API

class DestinationDetailAPIView(generics.RetrieveAPIView):

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]


# Destination Create API

class DestinationCreateAPIView(generics.CreateAPIView):

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAdminUser]


# Destination Update/Delete API

class DestinationUpdateDeleteAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAdminUser]
