import django
from django.db import models

from authentication.models import CustomUser as User


class PostComment(models.Model):
    """
    Модель, представляющая комментарий против блоге.
    """
    description = models.TextField(
        max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
       Строка для представления объектной модели.
        """
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring
