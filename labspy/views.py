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
# ============= standard library imports ========================
# ============= local library imports  ==========================
from django.views import generic


class Home(generic.TemplateView):
    template_name = 'home.html'


class People(generic.TemplateView):
    template_name = 'people.html'


class Hardware(generic.TemplateView):
    template_name = 'hardware.html'


class Software(generic.TemplateView):
    template_name = 'software.html'


class SoftwareMassSpec(generic.TemplateView):
    template_name = 'software_massspec.html'


LINKS = [('Source', 'https://github.com/NMGRL/pychron'),
         ('Documentation', 'http://pychron.readthedocs.org/en/latest/')
         ]


class SoftwarePychron(generic.TemplateView):
    template_name = 'software_pychron.html'

    def get_context_data(self, **kwargs):
        kwargs = super(SoftwarePychron, self).get_context_data(**kwargs)
        kwargs['links'] = LINKS
        return kwargs

# ============= EOF =============================================
