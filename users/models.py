from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=20)
    email = models.EmailField(unique=True, verbose_name='Email')
    mailings = models.IntegerField('Количество рассылок', default=0)
    avatar = models.ImageField('Изображение', upload_to='users/photo', blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name='Phone', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='City', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email