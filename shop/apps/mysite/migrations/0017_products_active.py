# Generated by Django 5.1.4 on 2025-01-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0016_alter_cart_options_remove_cart_counter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
