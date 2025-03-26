from users.models import CustomUser
from datetime import timedelta
from django.utils import timezone


def check_last_login():
    users = CustomUser.objects.all()

    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
        user.save()