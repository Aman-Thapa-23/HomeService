# Generated by Django 4.0 on 2022-12-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='is_complete',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete')], default='Incomplete', max_length=20),
        ),
    ]
