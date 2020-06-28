import platform
import uuid

import django
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
import os
from project.apps.curiosity.models import *


class Image(models.Model):
    id = models.SlugField("Интификатор", primary_key=True, editable=True)
    created_time = models.DateTimeField("Время создания", default=timezone.now)
    file = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True, blank=True)

    alt = models.CharField("Альтернативный текст", max_length=900, blank=True, null=True)

    url_prefix = models.CharField("Префикс", max_length=len(
        "https://dw8stlw9qt0iz.cloudfront.net/"), default="https://dw8stlw9qt0iz.cloudfront.net/")
    url = models.TextField(
        verbose_name="Ссылка", default=None, null=True)
    url_sufix = models.CharField(
        "Суфикс", max_length=len(".png"), default=".png")

    ROLE = (
        ('о', 'Обложка'),
        ('б1', "Блок 1"),
        ('б2', "Блок 2"),
        ('б3', "Блок 3"),
        ('б4', "Блок 4"),
        ('б5', "Блок 5"),
        ('б6', "Блок 6"),
        ('б8', "Блок 8"),
        ('б9', "Блок 9"),
        ('б10', "Блок 10"),
    )

    role = models.CharField(
        "Позиция",
        max_length=2,
        choices=ROLE,
        blank=True,
        default='о',
    )

    class Meta:
        ordering = ['created_time']

    def nice_x300_url(self, size):
        path_list = self.urls_x300.split(', ')
        return self.url_prefix + path_list[size] + self.url_sufix

    def nice_x600_url(self, size):
        path_list = self.urls_x600.split(', ')
        return self.url_prefix + path_list[size] + self.url_sufix

    def __str__(self):
        return str(self.id)
