import uuid
import os
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

def user_path(instance, filename):
    '''
        makes path  of the file using user id
    '''
    return 'userprofile/user_{0}/{1}'.format(instance.user.id, filename)

# Model for User avatar
class Picture(models.Model):
    '''
        model for storing UserProfile Avatar
    '''
    local_url = models.ImageField(upload_to=user_path)  # local url to the file
    url_to_upload = models.CharField(max_length=200, default='')  # url for front

    @staticmethod
    def upload_image(image):
        '''
            creates picture object
        '''
        picture = Picture.objects.create(
            local_url=image,
            url_to_upload=uuid.uuid4
        )
        return picture

    def delete(self, using=None, keep_parents=False):
        os.remove(self.local_url)
        super().delete(using=using, keep_parents=keep_parents)


class UserManager(BaseUserManager):
    '''
        Manager for custom User
    '''

    def create_user(self, username, email, password, **extra_fields):
        '''
            function that handle user creating
        '''

        if not email:
            raise ValueError("Email address is required field!")
        elif not username:
            raise ValueError("Username is required field!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        '''
            function that handle superuser creating
        '''

        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    '''
        Model for base User
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name="user name", max_length=200, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        '''
            Meta class for User
        '''

        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def has_perm(self, perm, obj=None):
        '''
            function that define permission
        '''
        return self.is_admin

    def has_module_perms(self, app_label):
        '''
            functuin that defin permission
        '''
        return self.is_admin

    def __str__(self):
        return f'{self.username}'


class UserProfile(models.Model):
    '''
        Model for User profile
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(verbose_name="user firstname", max_length=200, blank=True)
    surname = models.CharField(verbose_name="user surname", max_length=200, blank=True)
    avatar = models.ForeignKey(Picture, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'user'

    class Meta:
        '''
            Meat class for UserProfile
        '''

        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'
        ordering = ['-created_at']

    def set_avatar(self, avatar):
        '''
            sets userprofile avatar
        '''
        if self.avatar is not None:
            self.avatar.delete()
        self.avatar = Picture.upload_image(image=avatar)
        self.save()

    def __str__(self):
        if not self.firstname or not self.surname:
            return f'{self.user.username}'
        return f'{self.firstname} {self.surname}'
