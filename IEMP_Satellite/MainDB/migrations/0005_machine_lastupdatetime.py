# Generated by Django 3.2.6 on 2021-08-20 17:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainDB', '0004_remove_machine_lastupdatetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='LastUpdateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
