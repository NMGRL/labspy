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


class Connections(models.Model):
    appname = models.CharField(max_length=120)
    devname = models.CharField(max_length=120)
    com = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    status = models.BooleanField()


class Experiment(models.Model):
    system = models.CharField(max_length=80)
    name = models.CharField(max_length=140)
    user = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=datetime.now)
    state = models.CharField(max_length=80)


class Analysis(models.Model):
    experiment = models.ForeignKey(Experiment)
    runid = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=datetime.now)
    analysis_type = models.CharField(max_length=80)