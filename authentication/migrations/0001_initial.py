# Generated by Django 4.0 on 2022-06-13 14:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email_address')),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image')),
                ('is_customer', models.BooleanField(default=False)),
                ('is_worker', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkerRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='authentication.customuser')),
                ('experience', models.CharField(blank=True, choices=[('1 year', '1 year'), ('2 year', '2 year'), ('3 year', '3 year'), ('4 year', '4 year'), ('Above 5 year', 'Above 5 year')], default='Less than 1 year', max_length=50, null=True)),
                ('id_proof', models.CharField(blank=True, choices=[('Pan card', 'Pan card'), ('Citizenship', 'Citizenship'), ('Driving License', 'Driving License')], default='Citizenship', max_length=50, null=True)),
                ('id_image', models.ImageField(blank=True, null=True, upload_to='id_image')),
                ('user_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.workerrole')),
            ],
        ),
    ]
