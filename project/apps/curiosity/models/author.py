import django
from django.db import models

from authentication.models import CustomUser as User
from project.apps.curiosity.models import *


class PostAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(
        max_length=400, help_text="Введите био подробности здесь.")

    class Meta:
        ordering = ["user", "bio"]

    def get_absolute_url(self):
        """
        Возвращает URL для доступа конкретного экземпляра блог-автор.
        """
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объектной модели.
        """
        return self.user.username
