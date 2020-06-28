from django.db import models


class PageView(models.Model):
    ip = models.CharField(null=True, blank=True, max_length=32,)
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
