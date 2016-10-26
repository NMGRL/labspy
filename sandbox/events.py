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

import requests

def make_url(t, org=None):
    if org:
        tt = 'orgs/{}/{}'.format(org, t)
    else:
        tt = t

    return 'https://api.github.com/{}'.format(tt)

def get_events():
    url = make_url('events', 'NMGRLData')
    print url
    resp = requests.get(url)
    for i in resp.json():

        print i.keys(), i['type']
        # for c in i['payload']['commits']:
        #     print c['distinct'], c['message']

if __name__ == '__main__':
    get_events()
# ============= EOF =============================================
