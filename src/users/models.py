from django.db import models
from django.contrib.auth.hashers import make_password

class UserManager(models.Manager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The login field must be set')
        if password:
            password = make_password(password)
        user = self.model(login=login, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('role', 1)
        return self.create_user(login, password, **extra_fields)

class User(models.Model):
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=128)  # Ensure this length can store hashed passwords
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    password_restriction = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True) 

    objects = UserManager()

    def __str__(self):
        return self.login
    
    @property
    def is_authenticated(self):
        return True