from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(
        "Имя пользователя", max_length=20, blank=True, null=True
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        "Изображение", upload_to="users/photo", blank=True, null=True
    )
    phone = models.CharField(max_length=15, verbose_name="Phone", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="City", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


from lms.models import Course, Lesson


class Payment(models.Model):
    CHOICES = [("cash", "наличные"), ("transfer", "перевод")]
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    date = models.DateField("Дата оплаты", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    payment_summ = models.PositiveIntegerField("Сумма оплаты")
    session_id = models.CharField("ID сессии", max_length=255, blank=True, null=True)
    method = models.CharField("Способ оплаты", choices=CHOICES, max_length=20)
    link = models.URLField("Ссылка на оплату", max_length=400, blank=True, null=True)

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.session_id
