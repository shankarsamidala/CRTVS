# Generated by Django 4.1 on 2024-01-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_empname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoupload',
            name='upload_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
