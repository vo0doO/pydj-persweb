import django
from django.db import models


class Log(models.Model):
    text = models.TextField("Текст", max_length=5000, null=True)
    created_at = models.DateTimeField(
        "Дата обнаружения", auto_now=False, default=django.utils.timezone.now, blank=True)

    def __str__(self):
        return self.text
