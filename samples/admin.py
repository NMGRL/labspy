from django.contrib import admin

# Register your models here.

from .models import Sample, Material, Project

admin.site.register(Sample)
admin.site.register(Material)
admin.site.register(Project)