from django.db import models

class Counter(models.Model):
    amount = models.IntegerField(default=5)
