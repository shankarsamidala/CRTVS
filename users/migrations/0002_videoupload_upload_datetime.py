# Generated by Django 4.1 on 2024-01-09 07:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoupload',
            name='upload_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]