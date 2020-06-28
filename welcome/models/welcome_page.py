from django.db import models
from django.utils.translation import ugettext_lazy as _

from welcome.models.welcome_page_block import WelcomePageBlock


class WelcomePage(models.Model):
    name = models.CharField(_("Name"), blank=True, null=True, max_length=50)
    blocks = models.ManyToManyField(WelcomePageBlock)
    
    def __str__(self):
        return f"Страница: {self.name} id {self.id}"

    def write(self):
        self.object.save()
