# Generated by Django 4.0.5 on 2022-07-22 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assignment', '0005_serverrun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverrun',
            name='server',
            field=models.IntegerField(blank=True, choices=[(1, 'Not Run'), (2, 'Solo')], null=True),
        ),
    ]
