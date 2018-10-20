from django.db import models


# Create your models here.
class Filter(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'Filter'

    def __str__(self):
        return (self.name)


class Channel(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    filters = models.ManyToManyField(Filter)

    class Meta:
        db_table = 'Channel'

    def __str__(self):
        return (self.name)
