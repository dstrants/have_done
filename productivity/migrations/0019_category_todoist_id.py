# Generated by Django 3.0.7 on 2020-07-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0018_auto_20200722_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='todoist_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
