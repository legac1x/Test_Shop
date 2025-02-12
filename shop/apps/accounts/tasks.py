from shop.celery import app
from django.core.mail import send_mail
from django.conf import settings

@app.task
def user_confirm_task(email, url):
    sub = 'Подтверждение аккаунта'
    obj = f'Следуйте по этой ссылке, чтобы подтвердить свой аккаунт: {url}'
    send_mail(sub, obj, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)