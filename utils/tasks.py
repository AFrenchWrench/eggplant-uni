from celery import shared_task
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from graphql import GraphQLError
from redis import Redis


@shared_task
def send_email(to, subject, text):
    try:
        send_mail(
            subject,
            text,
            settings.EMAIL_HOST_USER,  # sender email
            [to],
            fail_silently=False,
        )
        return True
    except Exception as e:
        raise GraphQLError(str(e))


    # save token to redis and set expiration time 24 hours

