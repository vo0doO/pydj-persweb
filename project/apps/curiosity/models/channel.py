import django
from django.db import models

class Channel(models.Model):
    name = models.CharField("Русское название", null=True,
                            max_length=250, unique=True)
    name_en = models.CharField(
        "Английское название", null=True, max_length=250, unique=True)
    created_date = models.DateTimeField(
        "Даты создания", default=django.utils.timezone.now, blank=True)
    like = models.PositiveIntegerField("Лайк", default=0)

    def __str__(self):
        return self.name.capitalize()

