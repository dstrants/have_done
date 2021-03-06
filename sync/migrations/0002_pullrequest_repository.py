# Generated by Django 3.2.5 on 2021-07-22 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0029_alter_task_managers'),
        ('sync', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('private', models.BooleanField(default=False)),
                ('watch', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productivity.project')),
            ],
            options={
                'ordering': ('-watch', 'name'),
            },
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('html_url', models.URLField(blank=True, null=True)),
                ('title', models.CharField(default='Pull Request', max_length=400)),
                ('opened_by', models.CharField(default='gh-user', max_length=300)),
                ('user_url', models.URLField(blank=True, null=True)),
                ('status', models.CharField(default='open', max_length=50)),
                ('repo_name', models.CharField(max_length=100)),
                ('repo_full_name', models.CharField(max_length=200)),
                ('private', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('merged_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('number', 'repo_name')},
            },
        ),
    ]
