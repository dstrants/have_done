# Generated by Django 3.2.1 on 2021-05-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0012_repository_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='watch',
            field=models.BooleanField(default=False),
        ),
    ]
