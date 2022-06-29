# Generated by Django 4.0 on 2022-06-25 12:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0006_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('booking_time', models.CharField(choices=[('09am - 11am', '09am - 11am'), ('11am - 01pm', '11am - 01pm'), ('01pm - 03pm', '01pm - 03pm'), ('03pm - 05pm', '03pm - 05pm')], max_length=100, null=True)),
                ('problem_description', models.TextField()),
                ('problem_picture', models.ImageField(blank=True, null=True, upload_to='problem_picture')),
                ('is_accept', models.BooleanField(default=False)),
                ('is_denied', models.BooleanField(default=False)),
                ('accepted_date', models.DateTimeField(verbose_name=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('denied', 'denied'), ('accepted', 'accepted')], default='pending', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.worker')),
            ],
        ),
    ]
