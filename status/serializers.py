# ===============================================================================
# Copyright 2016 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
# ============= standard library imports ========================
# ============= local library imports  ==========================

# ============= EOF =============================================
from rest_framework import serializers

from status.models import Device, Measurement, ProcessInfo


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('name',)


class ProcessInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessInfo
        fields = ('name', 'units')


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    process_info = serializers.PrimaryKeyRelatedField(many=False, queryset=ProcessInfo.objects.all())

    class Meta:
        model = Measurement
        fields = ('value', 'process_info')
        # class Device(models.Model):
        #     name = models.CharField(max_length=80)
        #
        #     def __str__(self):
        #         return self.name
        #
        #
        # class ProcessInfo(models.Model):
        #     name = models.CharField(max_length=80)
        #     units = models.CharField(max_length=80)
        #     device = models.ForeignKey(Device)
        #
        #     def __str__(self):
        #         return '{} {} ({})'.format(self.device.name, self.name, self.units)
        #
        #
        # class Measurement(models.Model):
        #     process_info = models.ForeignKey(ProcessInfo)
        #     value = models.FloatField()
        #     pub_date = models.DateTimeField(default=datetime.now)
        #
        #     def __str__(self):
        #         re
