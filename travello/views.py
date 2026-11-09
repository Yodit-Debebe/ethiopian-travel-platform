from django.shortcuts import get_object_or_404, redirect, render

from travello.models import Destination
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import generics, filters
from .serializers import DestinationSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser

# Create your views here.

def home(request):
    destinations = Destination.objects.all()
    return render(request, 'home.html',{'destinations': destinations})


def welcome_page(request):
    return render(request, 'welcome.html')

@login_required(login_url='login')  # ⬅ user must login
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

        # Here you could save to DB or send an email
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('contact')  # Redirect to clear the form

    return render(request, "contact.html")


# API Views
class DestinationPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 6

class DestinationListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Destination.objects.all().order_by("id")
    serializer_class = DestinationSerializer
    pagination_class = DestinationPagination


    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Fields users can search
    search_fields = ["name", "desc"]

    # Fields users can use for sorting
    ordering_fields = ["name", "price", "id"]

    # Default sorting
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()

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

        return queryset



class DestinationDetailAPIView(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]


class DestinationCreateAPIView(generics.CreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAdminUser]
