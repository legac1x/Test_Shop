# Generated by Django 5.1.4 on 2025-01-09 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0015_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-create'], 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='counter',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(default=0, verbose_name='Колиечество товаров в корзине')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='mysite.cart', verbose_name='Корзина')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='mysite.products', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Товары в корзине',
                'ordering': ['counter'],
            },
        ),
    ]
