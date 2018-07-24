from django.db import models

class Upload(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    size = models.IntegerField()
    path = models.CharField(max_length=256)
