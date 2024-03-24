from django.core.mail import send_mail

def enviar_email(email, assunto, mensagem):
    send_mail(assunto, mensagem, 'carlospierre07@gmail.com', [email], fail_silently=False)
