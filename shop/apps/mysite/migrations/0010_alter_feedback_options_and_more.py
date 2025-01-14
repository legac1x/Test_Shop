# Generated by Django 5.1.4 on 2025-01-08 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_feedback_delete_specification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['-mark', '-create']},
        ),
        migrations.AddIndex(
            model_name='feedback',
            index=models.Index(fields=['-mark', '-create'], name='mysite_feed_mark_ebb2bb_idx'),
        ),
    ]
