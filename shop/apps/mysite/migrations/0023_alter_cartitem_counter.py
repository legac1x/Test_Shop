# Generated by Django 5.1.4 on 2025-02-02 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0022_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='Колиечество товара в корзине'),
        ),
    ]
