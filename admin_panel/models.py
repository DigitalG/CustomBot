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
        return (str(self.id) + self.name)


class Channel(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    forfilter = models.CharField(max_length=255,default='')
    filters = models.ManyToManyField(Filter)
    KeepForwardedCaption=models.BooleanField(default=True)

    class Meta:
        db_table = 'Channel'

    def __str__(self):
        return (self.name)


class Session(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=15)
    code = models.IntegerField(blank=True, null=True)
    self_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Session'

    def __str__(self):
        return (self.name)

class TeleBot(models.Model):
    token = models.CharField(max_length=255)