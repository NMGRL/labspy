from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

from django.db import models
from labman import settings


class Project(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material_detail', kwargs={'pk': self.pk})


class Sample(models.Model):
    name = models.CharField(max_length=80)
    project = models.ForeignKey(Project)
    material = models.ForeignKey(Material)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    worker = models.ForeignKey(User)
    sample = models.ForeignKey(Sample)

    def __str__(self):
        return '{} {}'.format(self.worker.username, self.sample.name)


class SamplePrep(models.Model):
    sample = models.ForeignKey(Sample)
    completed = models.BooleanField(default=False)

    crushed = models.BooleanField(default=False)
    sieved = models.BooleanField(default=False)
    frantz = models.BooleanField(default=False)
    hf = models.BooleanField(default=False)
    hl = models.BooleanField(default=False)
    hcl = models.BooleanField(default=False)

    crushed_note = models.TextField()
    sieved_note = models.TextField()
    frantz_note = models.TextField()
    hf_note = models.TextField()
    hl_note = models.TextField()
    hcl_note = models.TextField()
    general_note = models.TextField()
