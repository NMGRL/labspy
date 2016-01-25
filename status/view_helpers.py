# ===============================================================================
# Copyright 2016 Jake Ross
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
import time
import flot
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

# ============= local library imports  ==========================
from status.models import Connections


# bokeh graph
def make_bokeh_graph(data, title, ytitle):
    p = figure(title=title, x_axis_type='datetime', plot_height=300,
               tools='pan,box_zoom,reset,crosshair,hover')
    if data:
        xs, ys = zip(*[(m.pub_date, m.value) for m in data])
    else:
        xs, ys = [], []
    p.line(xs, ys)
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = ytitle
    j,d = components(p, CDN)
    return {'js':j, 'div':d}


# status
def make_current(ti, di, ui):
    obj = di.order_by('-pub_date').first()
    if obj is None:
        value = 0
        pub_date = ''
    else:
        value = obj.value
        pub_date = obj.pub_date
    return ti, value, ui, pub_date


def make_connections(name):
    return Connections.objects.filter(appname=name).values()


def connection_timestamp(name):
    f = Connections.objects.filter(appname=name).first()
    if f:
        return f.timestamp


def make_graph(data, fmt=None, options=None):
    if options == 'scatter':
        options = dict(points=dict(radius=1,
                                   show=True,
                                   fill=True,
                                   fillColor="#058DC7"),
                       color="#058DC7")
    else:
        options = dict(color='#238B45')

    if not fmt:
        fmt = '%H:%M:%S'

    yklass = flot.YVariable
    if data:
        xs, ys = zip(*[(m.pub_date, m.value) for m in data])
        if len(xs) > 5000:
            xs = xs[::5]
            ys = ys[::5]
        xklass = flot.TimeXVariable
    else:
        xs, ys = [0], [0]
        xklass = flot.XVariable

    # print xs,ys
    xx = xklass(points=xs)
    series1 = flot.Series(x=xx,
                          y=yklass(points=ys),
                          options=flot.SeriesOptions(**options))
    graph = flot.Graph(series1=series1,
                       options=flot.GraphOptions(xaxis={'mode': 'time',
                                                        'max': time.time() * 1000,
                                                        'min': xx.points[0],
                                                        'timezone': 'browser',
                                                        'timeformat': fmt}))
    return graph


# arar
def calculate_ideogram(ages, errors, n=500):
    from numpy import array, linspace, zeros, ones
    from numpy.core.umath import exp
    from math import pi

    ages, errors = array(ages), array(errors)
    lages = ages - errors * 2
    uages = ages + errors * 2

    xmax, xmin = uages.max(), lages.min()

    spread = xmax - xmin
    xmax += spread * 0.1
    xmin -= spread * 0.1

    bins = linspace(xmin, xmax, n)
    probs = zeros(n)

    for ai, ei in zip(ages, errors):
        if abs(ai) < 1e-10 or abs(ei) < 1e-10:
            continue

        # calculate probability curve for ai+/-ei
        # p=1/(2*pi*sigma2) *exp (-(x-u)**2)/(2*sigma2)
        # see http://en.wikipedia.org/wiki/Normal_distribution
        ds = (ones(n) * ai - bins) ** 2
        es = ones(n) * ei
        es2 = 2 * es * es
        gs = (es2 * pi) ** -0.5 * exp(-ds / es2)

        # cumulate probabilities
        # numpy element_wise addition
        probs += gs

    return tuple(bins), tuple(probs), xmin, xmax


def make_ideogram(ans):
    ages = [ai.age for ai in ans]
    age_errors = [ai.age_error for ai in ans]

    cumulative_prob = make_cumulative_prob(ages, age_errors)
    analysis_number = make_analysis_number(ages, age_errors)

    return cumulative_prob, analysis_number


def make_cumulative_prob(ages, age_errors):
    xs, ys, xmin, xmax = calculate_ideogram(ages, age_errors)
    xx = flot.XVariable(points=xs)
    yy = flot.YVariable(points=ys)

    series = flot.Series(x=xx, y=yy,
                         options=flot.SeriesOptions(color='blue'))

    cumulative_prob = flot.Graph(series1=series,
                                 options=flot.GraphOptions(xaxis={'max': xmax,
                                                                  'min': xmin},
                                                           yaxis={'show': False}))
    return cumulative_prob


def make_analysis_number(ages, age_errors):
    options = dict(points=dict(radius=2,
                               show=True,
                               fill=True,
                               fillColor='blue',
                               errorbars='x',
                               xerr={'show': True}),
                   color='blue')

    # print xs,ys
    data = zip(ages, age_errors)
    data = sorted(data, key=lambda x: x[0])
    ages, age_errors = zip(*data)

    ymax = len(ages) + 1
    ys = xrange(1, ymax)
    xx = flot.XVariable(points=ages)
    yy = flot.YVariable(points=ys)
    series = flot.Series(x=xx, y=yy, options=flot.SeriesOptions(**options))
    series['data'] = zip(ages, ys, age_errors)

    analysis_number = flot.Graph(series1=series)
    return analysis_number

# ============= EOF =============================================
