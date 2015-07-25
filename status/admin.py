from django.contrib import admin

# Register your models here.
from status.models import ProcessInfo, Measurement, Device

admin.site.register(Measurement)
admin.site.register(Device)
admin.site.register(ProcessInfo)