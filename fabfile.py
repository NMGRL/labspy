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
from fabric.api import local, lcd, cd, run
from fabric.state import env

env.hosts = ['argonlab4@argon158.nmt.edu']


def prepare_deploymoent(branch_name):
    # local('python manage.py test labspy')
    local('git add -p && git commit')


def deploy():
    with cd('~/Programming/labspy'):
        run('git pull origin master')

        # run('/anaconda/envs/labspy/bin/gunicorn labspy.wsgi --bind=129.138.12.158:8000')

        # local('python manage.py migrate labspy')
        # local('python manage.py test labspy')
        # run('gunicorn labspy.wsgi -bargon158.nmt.edu &')

# ============= EOF =============================================
