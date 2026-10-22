from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'register.html')

def login(request):
    next_url = request.GET.get('next') 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            return redirect(next_url or 'home')
        else:
            messages.error(request, 'Invalid username or password')

    if next_url:
        messages.warning(request, "Please log in to continue your payment.")

    return render(request, 'login.html')

