# Generated by Django 3.0.7 on 2020-08-04 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0023_auto_20200803_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task',
            field=models.CharField(max_length=400, unique=False),
        ),
    ]
