from calendar import month
from django.core.mail import send_mail
from pytz import timezone
from config.settings import EMAIL_HOST_USER
from celery import shared_task
from lms.models import Subscription

@shared_task
def check_course_update(pk):
    subs = Subscription.objects.filter(course_id=pk)

    for s in subs:
        send_mail(subject='Уведомление об обновлении курса',
                message=f'Курс {s.course.name}, на который вы подписаны, был обновлён',
                from_email=EMAIL_HOST_USER,
                recipient_list=[s.user.email])
        