# Generated by Django 4.0.5 on 2022-07-17 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Submit', '0003_submit_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='shortest_runtime',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.DeleteModel(
            name='SubmitResult',
        ),
    ]