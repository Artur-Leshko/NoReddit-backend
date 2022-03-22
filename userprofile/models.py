import uuid
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# def upload_to(instance, filename):
#     relative_path = instance.url_to_upload.rfind('images/') + len('images/')
#     return instance.url_to_upload[relative_path]

# Model for User avatar
# class Picture(models.Model):
    # local_url = models.ImageField(upload_to=upload_to)  # local url to the file
    # url_to_upload = models.Charfield(max_length=200, default='')  # url for front


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Email address is required field!")
        elif not username:
            raise ValueError("Useranem is required field!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    '''Model for User profile'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name="user name", max_length=200, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    firstname = models.CharField(verbose_name="user firstname", max_length=200, blank=True)
    surname = models.CharField(verbose_name="user surname", max_length=200, blank=True)
    # avatar = models.ForeignKey(Picture, )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
