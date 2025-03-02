from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, Payment
from users.serializers import PaymentSerializer, UserSerializer


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "method")
    ordering_fields = ("date",)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
