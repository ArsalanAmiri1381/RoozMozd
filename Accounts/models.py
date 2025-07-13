from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from timedelta import Timedelta


# ---------------------------------------------------
# 1. Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username required.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)




# ---------------------------------------------------
# 2. Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('worker', 'Worker'),
        ('employer', 'Employer'),
    )

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50 , null=True , blank=True)
    last_name = models.CharField(max_length=50 , null=True , blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True , null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # بعد از تایید OTP یا ایمیل
    national_id = models.CharField(max_length=11, unique=True)

    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



# ---------------------------------------------------
# 3. User profile
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=11, unique=True , null=True)
    address = models.TextField(blank=True, null=True)
    is_verified_identity = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)


# ---------------------------------------------------
# 4. OTP Model
class OTP(models.Model):
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=11, unique=True , null=True)
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < timezone.now() - Timedelta(minutes=2)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"


