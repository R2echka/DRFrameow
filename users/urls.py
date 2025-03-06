from django.db import router
from django.urls import path

from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import AllowAny, PaymentViewSet, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"payment", PaymentViewSet, basename="payment")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
] + router.urls
