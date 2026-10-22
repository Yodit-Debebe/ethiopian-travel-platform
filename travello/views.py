from django.shortcuts import get_object_or_404, redirect, render

from travello.models import Destination
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
