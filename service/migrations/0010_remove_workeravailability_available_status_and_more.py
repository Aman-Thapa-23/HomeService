# Generated by Django 4.0 on 2022-07-25 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_workeravailability'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workeravailability',
            name='available_status',
        ),
        migrations.AddField(
            model_name='workeravailability',
            name='unavailable_status',
            field=models.BooleanField(default=False, verbose_name='Make Unavailable'),
        ),
    ]
