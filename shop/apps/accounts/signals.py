from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.urls import reverse

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_confirm(sender, instance, *args, **kwargs):
    if not instance.is_verified:
        sub = 'Подтверждение аккаунта'
        url = reverse('verify', kwargs={'uuid': str(instance.verified_uuid)})
        full_url = f'http://localhost:8000{url}'
        obj = f'Следуйте по этой ссылке, чтобы подтвердить свой аккаунт: {full_url}'
        send_mail(sub, obj, settings.DEFAULT_FROM_EMAIL, [instance.email], fail_silently=False)
