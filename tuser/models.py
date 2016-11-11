from django.db import models
from django.contrib.auth.models import AbstractUser
from django_mysql.models import JSONField

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    sidebar_menu_top = JSONField()
    sidebar_menu_bottom = JSONField()

