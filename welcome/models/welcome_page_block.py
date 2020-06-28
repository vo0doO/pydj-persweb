from django.db import models
from django.utils.translation import ugettext_lazy as _


class WelcomePageBlock(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    link_text = models.CharField(_("Link text"), max_length=250)
    link_url = models.CharField(_("Link url"), max_length=250) 

    def __str__(self):
        return f"{self.id} {self.title}"

    def write(self):
        self.object.save()
