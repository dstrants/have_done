# Generated by Django 2.2.6 on 2020-05-25 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0016_taskaddonprovider_shortcut'),
        ('logs', '0009_auto_20200212_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productivity.Project'),
        ),
    ]
