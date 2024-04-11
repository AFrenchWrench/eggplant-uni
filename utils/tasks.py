from celery import shared_task
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from redis import Redis


@shared_task
def send_email(to, subject, text):
    token = get_random_string(length=32)
    send_mail(
        subject,
        text + f' This is your token: {token}',
        settings.EMAIL_HOST_USER,  # sender email
        [to],
        fail_silently=False,
    )

    # save token to redis and set expiration time 24 hours
    r = Redis(host='localhost', port=6379, db=0)
    r.set(token, to)
    r.expire(token, 60 * 60 * 24)  #Expire Token After 24H
