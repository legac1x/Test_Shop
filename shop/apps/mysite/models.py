from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from mptt.models import TreeForeignKey, MPTTModel
from apps.services.utils import unique_slugify
from django.contrib.auth.models import User


class ProductsIsPresent(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='present')

class Products(models.Model):

    STATUS_OPTION = (
         ('present', 'Присутствует'),
         ('sold_out', 'Распродано')
    )

    title = models.CharField(max_length=50, verbose_name='Название товара')
    slug = models.SlugField(verbose_name='URL', blank=True, max_length=255)
    body = models.TextField(verbose_name='Описание товара', blank=True)
    thumbnail = models.ImageField(default='default.jpg',
                                  verbose_name='Изображение товара',
                                  blank=True,
                                  upload_to='images/thumbnails/%Y/%m/%d/',
                                  validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpg', 'jpeg'])])
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products',
                              verbose_name='Категория')
    price = models.CharField(max_length=10, verbose_name='Цена')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    status = models.CharField(choices=STATUS_OPTION, max_length=12, default='present', verbose_name='Статус')
    active = models.BooleanField(default=True)
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                related_name='updater_product', blank=True, verbose_name='Обновил')

    objects = models.Manager()
    custom = ProductsIsPresent()

    class Meta:
        ordering = ['status']
        indexes = [models.Index(fields=['status', '-create'])]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('products_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    MARKS_OPTION = (('1', '1'),
                    ('2', '2'),
                    ('3', '3'),
                    ('4', '4'),
                    ('5', '5'))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукт', related_name='feedbacks')
    name = models.CharField(max_length=80, blank=True, verbose_name='Имя')
    body = models.TextField(verbose_name='Текст отзыва')
    mark = models.CharField(max_length=1, choices=MARKS_OPTION, verbose_name='Оценка')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания оценки')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления оценки')

    class Meta:
        ordering = ['-mark', '-create']
        indexes = [models.Index(fields=['-mark', '-create'])]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.mark} by {self.name}'

class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        ordering_insertion_by = ('title', )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'shop_categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='carts')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания корзины')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления корзины')

    class Meta:
        ordering = ['-create']
        indexes = [models.Index(fields=['-create'])]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart', verbose_name='Корзина')
    item = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products', verbose_name='Товары')
    counter = models.IntegerField(default=0, verbose_name='Колиечество товара в корзине')

    class Meta:
        ordering = ['counter']
        verbose_name = 'Товары в корзине'

    def __str__(self):
        return f'{self.item}'
