# Generated by Django 3.0.7 on 2020-08-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0024_auto_20200804_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task',
            field=models.CharField(max_length=400),
        ),
    ]
