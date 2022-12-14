# Generated by Django 4.0.5 on 2022-07-10 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.CharField(blank=True, max_length=1000, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(blank=True, max_length=1000, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Female'), (2, 'Male'), (3, 'Other')], null=True)),
                ('total_assigment', models.IntegerField(blank=True, default=0, null=True)),
                ('total_challenge', models.IntegerField(blank=True, default=0, null=True)),
                ('total_group', models.IntegerField(blank=True, default=0, null=True)),
                ('total_score', models.IntegerField(blank=True, default=0, null=True)),
                ('assignment_easy', models.IntegerField(blank=True, default=0, null=True)),
                ('assignment_medium', models.IntegerField(blank=True, default=0, null=True)),
                ('assignment_hard', models.IntegerField(blank=True, default=0, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.account')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.organization')),
            ],
        ),
    ]
