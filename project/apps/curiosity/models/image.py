import platform
import uuid

import django
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

from project.apps.curiosity.models import *


class Image(models.Model):
    id = models.SlugField("Интификатор", primary_key=True, editable=True)
    created_time = models.DateTimeField("Время создания", default=timezone.now)
    
    post = models.ForeignKey(
        "Post",
        on_delete=models.SET_NULL,
        verbose_name="Пост",
        null=True
        )

    url_prefix = models.CharField("Префикс", max_length=len(
        "https://dw8stlw9qt0iz.cloudfront.net/"), default="https://dw8stlw9qt0iz.cloudfront.net/")
    urls_x300 = models.TextField(
        verbose_name="Размеры x300", default=None, null=True)
    urls_x600 = models.TextField(
        verbose_name="Размеры x600", default=None, null=True)
    url_sufix = models.CharField(
        "Суфикс", max_length=len(".png"), default=".png")

    ROLE = (
        ('о', 'Обложка'),
        ('б1', "Блок 1"),
        ('б2', "Блок 2"),
        ('б3', "Блок 3"),
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

    def get_storage(unix_pref, windows_pref):
        plat = platform.system()
        if plat == "Windows":
            return FileSystemStorage(location=os.path.join(windows_pref, "media"))
        elif plat != "Linux":
            return FileSystemStorage(location=os.path.join(unix_pref, "media"))
        else:
            return FileSystemStorage(location="")

    def get_path(self):
        pass
        #     if self.img:
        #         return mark_safe(str(self.img.path))
        #     else:
        #         return 'none'
        # display_img_path.short_description = 'Путь к изображению'
        # display_img_path.allow_tags = True

    def __str__(self):
        return str(self.id)
