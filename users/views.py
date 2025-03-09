from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from django.utils import timezone

from users.models import CustomUser, Payment
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_price, create_stripe_product, create_stripe_session


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "method")
    ordering_fields = ("date",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, date = timezone.now().date())
        product = create_stripe_product(payment)
        price = create_price(payment.payment_summ, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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
