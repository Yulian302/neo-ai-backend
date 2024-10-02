from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.user.exceptions import UserExistsException


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError(
                "Incorrect username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is disabled.")
        return {"user": user}


class OAuth2LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs["username"])
        if not user:
            raise serializers.ValidationError(
                "User could not be found!")
        if not user.is_active:
            raise serializers.ValidationError("User is disabled.")
        return {"user": user}


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["repeat_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields must match"}
            )
        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"])
            user.set_password(validated_data["password"])
            user.save()
        except:
            raise UserExistsException("User already exists")
        return user


class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
