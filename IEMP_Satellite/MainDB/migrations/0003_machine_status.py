# Generated by Django 3.2.6 on 2021-08-20 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainDB', '0002_machine'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='Status',
            field=models.IntegerField(default=0),
        ),
    ]
