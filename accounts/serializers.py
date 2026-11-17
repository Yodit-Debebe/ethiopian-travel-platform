from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value

    def validate(self, attrs):
        candidate = User(
            username=attrs.get("username"),
            email=attrs.get("email")
        )

        try:
            validate_password(attrs.get("password"), user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": list(error.messages)}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        attrs["user"] = user
        return attrs

class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
    user = UserResponseSerializer()


class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = UserResponseSerializer()


class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        write_only=True,
        required=False,
        allow_null=True
    )

    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
            "profile_picture_url",
        ]
        read_only_fields = ["id", "profile_picture_url"]

    def validate_username(self, value):
        user = self.instance

        if User.objects.filter(username=value).exclude(
            id=user.id
        ).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )

        return value

    def validate_email(self, value):
        user = self.instance

        if value and User.objects.filter(email__iexact=value).exclude(
            id=user.id
        ).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def get_profile_picture_url(self, obj) -> str | None:
        profile = Profile.objects.filter(user=obj).first()

        if not profile or not profile.profile_picture:
            return None

        request = self.context.get("request")
        picture_url = profile.profile_picture.url

        if request:
            return request.build_absolute_uri(picture_url)

        return picture_url

    def update(self, instance, validated_data):
        picture = validated_data.pop(
            "profile_picture",
            serializers.empty
        )

        instance = super().update(instance, validated_data)

        if picture is not serializers.empty:
            profile, created = Profile.objects.get_or_create(
                user=instance
            )

            profile.profile_picture = picture
            profile.save()

        return instance