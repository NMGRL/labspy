from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

from django.db import models


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
