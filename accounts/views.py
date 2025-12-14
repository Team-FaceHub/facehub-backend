from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


from .serializers import RegisterSerializer, LoginSerializer
from .utils import get_tokens_for_user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = get_tokens_for_user(user)

        user_data = {
            "id": user.id,
            "email": getattr(user, "email", None),
            "role": getattr(user, "role", None),
            "is_verified": getattr(user, "is_verified", False),
        }

        return Response(
            {
                "user": user_data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        tokens = get_tokens_for_user(user)

        user_data = {
            "id": user.id,
            "email": getattr(user, "email", None),
            "role": getattr(user, "role", None),
            "is_verified": getattr(user, "is_verified", False),
        }

        return Response(
            {
                "user": user_data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": getattr(user, "email", None),
            "role": getattr(user, "role", None),
            "is_verified": getattr(user, "is_verified", False),
        }
        return Response(data, status=status.HTTP_200_OK)
