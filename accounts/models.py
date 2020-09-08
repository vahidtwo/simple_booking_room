from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator

from core import model


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, phone_number, **extra_fields):
        if not username:
            raise ValueError('username must be set')
        if not password:
            raise ValueError('password must be set')
        if not phone_number:
            raise ValueError('phone_number must be set')

        username = self.model.normalize_username(username)
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(username, password, phone_number, **extra_field)

    def create_staff(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(username, password, phone_number, **extra_field)

    def create_superuser(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        return self._create_user(username, password, phone_number, **extra_field)


class User(AbstractBaseUser, model.AbstractBaseModel, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="number must be entered in the format: '+9...' 9 Up to 15 digits allowed.")
    username = model.CharField(max_length=150, unique=True)
    email = model.CharField(max_length=150, null=True, blank=True, validators=[EmailValidator])
    first_name = model.CharField(max_length=50, null=True)
    last_name = model.CharField(max_length=50, null=True)
    phone_number = model.CharField(max_length=15, unique=True, validators=[phone_regex])
    gender = model.BooleanField(default=True)
    birthday = model.DateField(null=True)
    is_staff = model.BooleanField(default=False)
    is_superuser = model.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']
