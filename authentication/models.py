from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    fav_color = models.CharField(max_length=120, blank=True, null=True)
