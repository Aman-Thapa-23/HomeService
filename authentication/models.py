from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password, address, phone_number, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email,
                          name=name,
                          address=address,
                          phone_number=phone_number,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    email = models.EmailField(_('email_address'), max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=100)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_image')
    is_customer = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'
 

class WorkerCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Worker(models.Model):
    EXPERIENCE = (
            ("1 year", "1 year"),
            ("2 year", "2 year"),
            ("3 year", "3 year"),
            ("4 year", "4 year"),
            ("Above 5 year", "Above 5 year"),
        )
    ID_PROOF = (
            ('Pan card', 'Pan card'),
            ('Citizenship', 'Citizenship'),
            ('Driving License', 'Driving License'),
        )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    experience = models.CharField(choices=EXPERIENCE, max_length=50, default="Less than 1 year", null=True, blank=True)
    id_proof = models.CharField(choices=ID_PROOF, max_length=50, default='Citizenship', null=True, blank=True)
    id_image = models.ImageField(null=True, blank=True, upload_to='id_image')
    category_name = models.ForeignKey(WorkerCategory, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return f'{self.user}'