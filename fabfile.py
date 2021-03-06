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

env.hosts = ['jross@129.138.12.10']
env.project_root = '/home/jross/web/labspy'
env.bin = '/home/jross/anaconda/envs/labspy/bin'

def prepare_deploymoent(branch_name):
    # local('python manage.py test labspy')
    local('git add -p && git commit')


def deploy():
    with cd(env.project_root):
        run('git pull origin master')
        run('{}/pip install -r requirements.txt'.format(env.bin))
        run('{}/python manage.py migrate'.format(env.bin))
        run('{}/python manage.py bower install'.format(env.bin))
        run('{}/python manage.py collectstatic -v0 --noinput'.format(env.bin))
        # run('/anaconda/envs/labspy/bin/gunicorn labspy.wsgi --bind=129.138.12.158:8000')

        # local('python manage.py test labspy')
        # run('gunicorn labspy.wsgi -bargon158.nmt.edu &')

# ============= EOF =============================================
