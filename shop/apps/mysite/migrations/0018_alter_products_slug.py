# Generated by Django 5.1.4 on 2025-01-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0017_products_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='URL'),
        ),
    ]
