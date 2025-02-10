from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from .models import Cart, Products
from django.core.cache import cache


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=Products)
def update_products_list_cache(sender, instance, **kwargs):
    products_list = list(Products.objects.all())
    cache.set('products_list', products_list, timeout=600)

@receiver(post_delete, sender=Products)
def delete_products_out_of_cache(sender, instance, **kwargs):
    cache.delete('products_list')