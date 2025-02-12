from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
from django.urls import reverse
from .tasks import user_confirm_task

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_confirm(sender, instance, *args, **kwargs):
    if not instance.is_verified:
        url = reverse('verify', kwargs={'uuid': str(instance.verified_uuid)})
        full_url = f'http://localhost:8000{url}'
        user_confirm_task.delay(instance.email, full_url)
