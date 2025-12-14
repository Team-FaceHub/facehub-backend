from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Prosty serializer do rejestracji, NIE oparty o ModelSerializer,
    więc nie obchodzi go, jakie dokładnie pola ma model User.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.get("email")
        role = validated_data.get("role", None)

        user = User(email=email)

        # Ustawiamy role tylko jeśli model faktycznie ma takie pole
        if role and hasattr(user, "role"):
            user.role = role

        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Podaj email i hasło.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Nieprawidłowy email lub hasło.")

        if not user.check_password(password):
            raise serializers.ValidationError("Nieprawidłowy email lub hasło.")

        if not getattr(user, "is_active", True):
            raise serializers.ValidationError("Konto jest nieaktywne.")

        attrs["user"] = user
        return attrs
