from django.contrib import admin
from .models import Products, Feedback, Category, Cart, CartItem
from django_mptt_admin.admin import DjangoMpttAdmin

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'create', 'status']
    list_filter = ['status', 'create', 'update']
    prepopulated_fields = {'slug': ('title', )}

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'mark']

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title', )}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass