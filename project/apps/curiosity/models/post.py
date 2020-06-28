import os
import re
from urllib.parse import urlparse

import django
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import mark_safe
from parso.python.diff import DiffParser

from authentication.models import CustomUser as User
from project.apps.curiosity.models.author import PostAuthor
from project.apps.curiosity.models.channel import Channel
from project.apps.curiosity.models.comment import PostComment
from project.apps.curiosity.models.image import Image as CImage
from project.apps.curiosity.models.log import Log
from project.apps.curiosity.models.tag import Tag


class Post(models.Model):

    author = models.ForeignKey(
        PostAuthor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title_en = models.CharField(
        "Английский аголовок",
        max_length=500,
        unique=True,
        null=True
    )

    text_en = models.TextField(
        "Английский текст",
        null=True
    )

    title = models.CharField(
        "Заголовок",
        max_length=500,
        unique=True,
        null=True
    )

    html = models.TextField(
        "ХТМЛ",
        null=True
    )

    url = models.URLField(
        verbose_name="Источник",
        null=True,
    )

    text = models.TextField(
        "Русский текст",
        null=True
    )

    channel = models.ForeignKey(
        "Channel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Рубрика"
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name="Хештеги"
    )

    created_date = models.DateTimeField(
        "Дата создания",
        auto_now=False,
        default=django.utils.timezone.now,
        blank=True
    )

    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=False,
        null=True,
        blank=True,
    )

    rewrite_date = models.DateTimeField(
        "Дата редактирования",
        null=True,
        auto_now=True,
    )

    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )

    img = models.ForeignKey(
        CImage,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Первое изображение",
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    
    FINDED = "Обнаружен"

    PUBLISHED = "Опубликован"

    STATUS = (
        (FINDED, "FINDED"),
        (PUBLISHED, "PUBLISHED"),
    )

    status = models.CharField(
        "Статус",
        max_length=15,
        choices=STATUS,
        null=False,
        default="Обнаружен"
    )

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("curiosity:post-detail", args=(self.slug,)[1:]))

    def display_tag(self):
        return ', '.join([tag.name for tag in self.tags.all()[:]])
    display_tag.short_description = "Хештеги"

    def display_image(self):
        if self.slug:
            return mark_safe('<img src="http://io.net.ru:1443/img/%s.png_draws.png" width="96" height="96"></img>' % self.slug)
        else:
            return 'none'
    display_image.short_description = 'Изображение'
    display_image.allow_tags = True

    def format_html(self):
        soup = BeautifulSoup(self.html, "lxml")
        
        imgs = soup.findAll({"img": "href"})
        for img in imgs:
            img["src"] = str("http://www.discoverychannel.ru" + img["src"])

    @property
    def is_readypub(self):
        if self.text and self.title and self.img:
            return True
        return False

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-created_date"]
        permissions = (('can_mark_returned', 'Can mark returned'),)

    # def clean(self) -> None:

    #     try:
    #         if self.author is not None:
    #             print(f"{self.author} is author field")
    #         else:
    #             raise ValidationError(f"{self.author} field is not Validate")

    #         if self.title is not None:
    #             print(f"{self.title} is title field")
    #         else:
    #             raise ValidationError(f"{self.title} field is not Validate")

    #         if self.text is not None:
    #             print(f"{self.text} is text field")
    #         else:
    #             raise ValidationError(f"{self.text} field is not Validate")

    #         if self.title is not None:
    #             print(f"{self.title} is title field")
    #         else:
    #             raise ValidationError(f"{self.title} field is not Validate")

    #         if self.html is not None:
    #             print(f"{self.html} is html field")
    #         else:
    #             raise ValidationError(f"{self.html} field is not Validate")

    #         if self.url is not None:
    #             print(f"{self.url} is url field")
    #         else:
    #             raise ValidationError(f"{self.url} field is not Validate")

    #         if self.text is not None:
    #             print(f"{self.text} is text field")
    #         else:
    #             raise ValidationError(f"{self.text} field is not Validate")

    #         if self.channel is not None:
    #             print(f"{self.channel} is channel field")
    #         else:
    #             raise ValidationError(f"{self.channel} field is not Validate")

    #         if self.tags is not None:
    #             print(f"{self.tags} is tags field")
    #         else:
    #             raise ValidationError(f"{self.ags} field is not Validate")

    #         if self.created_date is not None:
    #             print(f"{self.created_date} is created field")
    #         else:
    #             raise ValidationError(
    #                 f"{self.created_date} field is not Validate")

    #         if self.pub is not None:
    #             print(f"{self.pub} is pub field")
    #         else:
    #             raise ValidationError(f"{self.pub_date} field is not Validate")

    #         if self.self.rewrite is not None:
    #             print(f"{self.rewrite} is rewrite field")
    #         else:
    #             raise ValidationError(f"{self.rewrite} field is not Validate")

    #         if self.slug is not None:
    #             print(f"{self.slug} is slug field")
    #         else:
    #             raise ValidationError(f"{self.slug} field is not Validate")

    #         if self.img is not None:
    #             print(f"{self.img} is img field")
    #         else:
    #             raise ValidationError(f"{self.img} field is not Validate")
    #     except Exception as error:
    #         print(f"Error: {error.args}")
    #         self.publish_post()

if __name__ == "__main__":
    pass
