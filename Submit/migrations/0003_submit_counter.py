# Generated by Django 4.0.5 on 2022-07-17 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Submit', '0002_remove_submit_assignment_remove_submit_challenge_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='counter',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
