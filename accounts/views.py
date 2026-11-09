
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    LoginResponseSerializer,
    RegisterResponseSerializer,
    LogoutResponseSerializer,
)


# -------------------------
# Template-based views
# -------------------------

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
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(
                    request,
                    'Registration successful! You can now log in.'
                )
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')


def login(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url or 'home')
        else:
            messages.error(request, 'Invalid username or password')

    if next_url:
        messages.warning(
            request,
            "Please log in to continue your payment."
        )

    return render(request, 'login.html')


# -------------------------
# Registration API
# -------------------------

@extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterResponseSerializer},
    description="Register a new user account.",
    tags=["Authentication"],
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# -------------------------
# Login API
# -------------------------

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: OpenApiResponse(
                description="Invalid username or password."
            ),
        },
        description="Authenticate a user and return an API token.",
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Login successful.",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


# -------------------------
# Logout API
# -------------------------

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: LogoutResponseSerializer,
            401: OpenApiResponse(
                description=(
                    "Authentication credentials were not provided "
                    "or are invalid."
                )
            ),
        },
        description="Log out the authenticated user by deleting their API token.",
        tags=["Authentication"],
    )
    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK
        )
