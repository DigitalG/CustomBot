from django.db import models


# Create your models here.
class Filter(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
