from datetime import datetime
from django.db import models


# Create your models here.


class Device(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class ProcessInfo(models.Model):
    name = models.CharField(max_length=80)
    units = models.CharField(max_length=80)
    device = models.ForeignKey(Device)

    def __str__(self):
        return '{} {} ({})'.format(self.device.name, self.name, self.units)


class Measurement(models.Model):
    process_info = models.ForeignKey(ProcessInfo)
    value = models.FloatField()
    pub_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return '{}: {}'.format(self.process_info.name, self.value)


class CurrentExperiment(models.Model):
    system = models.CharField(max_length=80)
    name = models.CharField(max_length=140)
    user = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=datetime.now)


class CurrentAnalysis(models.Model):
    experiment = models.ForeignKey(CurrentExperiment)
    runid = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=datetime.now)
