# Generated by Django 2.2.6 on 2020-02-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0005_auto_20190920_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('title', models.CharField(default='Pull Request', max_length=400)),
                ('opened_by', models.CharField(default='gh-user', max_length=300)),
                ('status', models.CharField(default='open', max_length=50)),
                ('repo_name', models.CharField(max_length=100)),
                ('repo_full_name', models.CharField(max_length=200)),
                ('private', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('merged_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
