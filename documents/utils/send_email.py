from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from celery import shared_task

def enviar_email(assunto, mensagem):
    send_mail(
        assunto,
        mensagem,
        EMAIL_HOST_USER,
        ['pierre.br18@gmail.com'],
        fail_silently=False,
    )

    return "Done"