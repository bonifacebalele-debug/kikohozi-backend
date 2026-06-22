import logging
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.mobile.auth import CsrfExemptSessionAuthentication
from apps.mobile.throttles import LoginRateThrottle

logger = logging.getLogger(__name__)


def user_to_dict(user):
    return {
        "id": user.pk,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "groups": list(user.groups.values_list("name", flat=True)),
    }


class StatusView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "success": True,
            "message": "Service is running.",
            "data": {
                "service": "Kikohozi Mobile API",
                "status": "ok",
                "authenticated": request.user.is_authenticated,
            },
        })


class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")

        if not username or not password:
            return Response(
                {"success": False, "message": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            logger.warning(
                "Failed login attempt for username=%s",
                username,
                extra={"request_id": getattr(request, "request_id", "-")},
            )
            return Response(
                {"success": False, "message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"success": False, "message": "This account has been disabled."},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user)
        logger.info(
            "User %s logged in",
            username,
            extra={"request_id": getattr(request, "request_id", "-")},
        )

        return Response({
            "success": True,
            "message": "Login successful.",
            "data": {"user": user_to_dict(user)},
        })


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        return Response({"success": True, "message": "Logged out successfully."})


class MeView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        return Response({
            "success": True,
            "message": "Authenticated user retrieved.",
            "data": {"user": user_to_dict(request.user)},
        })
