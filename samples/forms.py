# ===============================================================================
# Copyright 2015 Jake Ross
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
# ============= local library imports  ==========================
from django.forms import ModelForm
from samples.models import Sample, Material, Project, Assignment, SamplePrep


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('name',)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ('name', 'material', 'project')


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ('sample', 'worker')


class SamplePrepForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SamplePrepForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = SamplePrep
        fields = ('sample','crushed', 'sieved', 'frantz', 'hf', 'hl', 'hcl', 'crushed_note', 'sieved_note', 'frantz_note',
                  'hf_note', 'hl_note', 'hcl_note', 'general_note')

# ============= EOF =============================================
