from django.db import models


class AppData(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)