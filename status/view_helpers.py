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
import string
import time
import math
from collections import namedtuple

import flot
from datetime import datetime, timedelta
from django import forms
from numpy import array, histogram, argmax, hanning, ones, asarray, r_, convolve
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

# ============= local library imports  ==========================
from status.models import Connections, Measurement

# bokeh graph
DataPoint = namedtuple('DataPoint', 'pub_date value')

DS = [{"hours": 1}, {'hours': 24}, {'weeks': 1}, {'weeks': 4}]
FMTS = ['%M:%S', '%H:%M', '%m/%d', '%m/%d']


class DateSelectorForm(forms.Form):
    date_range_name = forms.ChoiceField(label='', choices=(('0', 'Last Hour'),
                                                           ('1', 'Last Day'),
                                                           ('2', 'Last Week'),
                                                           ('3', 'Last Month')),
                                        initial='1')
    use_last = forms.BooleanField(initial=True,
                                  required=False)

    low_post = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',)) #widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    high_post = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',)) #widget=forms.widgets.DateInput(format="%m/%d/%Y"))


def floatfmt(f, n=4, s=4, max_width=None, default='NaN', use_scientific=True):
    """
        f: value to format
        n: number of sig figs

        use scientific notation
        if f<10^-n (e.g n=#.## f=0.00001)
        or
        f>10^(s+1) (e.g  s=### f=3001)

    """
    if isinstance(f, str):
        return f
    if f is None:
        return default

    absf = abs(f)
    if absf < 1e-20:
        v = '0.0'
    else:
        if absf < math.pow(10, -n) or absf > math.pow(10, s + 1):
            if use_scientific:
                fmt = '{{:0.{}E}}'.format(s)
            else:
                if absf < math.pow(10, s + 1):
                    # f = Decimal(f)
                    # n = int(math.ceil(abs(math.log10(absf))))
                    n = int(round(abs(math.log10(absf))))

                fmt = '{{:0.{}f}}'.format(n)

        else:
            fmt = '{{:0.{}f}}'.format(n)

        v = fmt.format(f)
        if max_width:
            if len(v) > max_width:
                v = v[:max_width]

    return v


def calc_bloodtest(name, data):
    mi, ma, mean, std, latest, timestamp = 0, 0, 0, 0, 0, ''
    if data:
        if isinstance(data, list):
            la = data[-1]
        else:
            la = data.last()

        latest = la.value
        timestamp = la.pub_date

        data = array([di.value for di in data])
        mi = data.min()
        ma = data.max()
        mean = data.mean()
        std = data.std()

    bd = {'name': name,
          'min': floatfmt(mi),
          'max': floatfmt(ma),
          'mean': floatfmt(mean),
          'std': floatfmt(std),
          'latest': floatfmt(latest),
          'timestamp': timestamp}

    return bd


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_post(request):

    if request.method == 'POST':
        form = DateSelectorForm(request.POST)
        print 'asfasf', form.is_valid()
        if form.is_valid():

            if form.cleaned_data['use_last']:
                d = int(form.cleaned_data['date_range_name'])
                high = datetime.now()
                low = high - timedelta(**DS[d])
            else:
                low = form.cleaned_data['low_post']
                high = form.cleaned_data['high_post']
        else:
            print form.errors
    else:
        form = DateSelectorForm()
        high = datetime.now()
        low = high - timedelta(**DS[1])

    # if not dt:

    # now = datetime.now()
    # post = (now - dt)
    return (high, low), form


def get_data(table, post):
    high, low = post
    print high, low
    data = table.filter(pub_date__gte=low).filter(pub_date__lte=high).all()
    if not data or len(data) == 1:
        v = table.order_by('pub_date').last()
        if v:
            data = [v, DataPoint(datetime.now(), v.value)]
    return data


def smooth(x, window_len=11, window='flat'):
    x = asarray(x)
    s = r_[2 * x[0] - x[window_len - 1::-1], x, 2 * x[-1] - x[-1:-window_len:-1]]

    if window == 'flat':  # moving average
        w = ones(window_len, 'd')
    else:
        if window == 'hanning':
            w = hanning(window_len)
        # mod = __import__('numpy', fromlist=[window])
        # func = getattr(mod, window)
        # w = func(window_len)
        # w = eval('np.' + window + '(window_len)')

    y = convolve(w / w.sum(), s, mode='same')
    return y[window_len:-window_len + 1]


def make_bokeh_graph(data, title, ytitle):
    p = figure(title=title, x_axis_type='datetime',
               plot_width=450,
               plot_height=250,
               background_fill="beige",
               tools='pan,box_zoom,reset,save')
    if data:
        xs, ys = zip(*[(m.pub_date, m.value) for m in data])
        p.line(xs, ys, line_width=2)
        p.line(xs, smooth(ys), line_width=4, line_color='orange', line_dash='dashed')

    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = ytitle
    return _make_bokeh_components(p)


def _make_bokeh_components(p):
    j, d = components(p, CDN)
    return {'js': j, 'div': d}


# spectrometer
def make_spectrometer_dict(name):
    trap = Measurement.objects.filter(process_info__name='{}TrapCurrent'.format(name))
    emission = Measurement.objects.filter(process_info__name='{}Emission'.format(name))
    decabin = Measurement.objects.filter(process_info__name='{}DecabinTemp'.format(name))

    trap_current = trap.order_by('pub_date').last()
    source_emission = emission.order_by('pub_date').last()
    decabin_temp = decabin.order_by('pub_date').last()

    trap_current_flag = False
    if trap_current:
        date = trap_current.pub_date.strftime('%m/%d %H:%M')
        vs = get_vs(trap)
        trap_value, trap_current_flag = make_value(vs, trap_current.value)
    else:
        trap_value = '---'
        date = ''

    emission_flag = False
    if source_emission:
        vs = get_vs(emission)
        emission_value, emission_flag = make_value(vs, source_emission.value)
    else:
        emission_value = '---'

    decabin_flag = False
    if decabin_temp:
        vs = get_vs(decabin)
        decabin_temp_value, decabin_flag = make_value(vs, decabin_temp.value)

    else:
        decabin_temp_value = '---'

    trap_ratio = '---'
    emission_ratio_flag = False
    if emission_value != '---' and trap_value != '---':
        er = source_emission.value / trap_current.value
        # ts = trap.order_by('-pub_date')[1:50]
        # es = emission.order_by('-pub_date')[1:50]
        es, ts = get_vs(emission), get_vs(trap)
        rs = [ei / ti for ei, ti in zip(es, ts)]

        trap_ratio, emission_ratio_flag = make_value(rs, er)

    return {'name': name, 'date': date,
            'trap_current': trap_value,
            'emission': emission_value,
            'decabin_temp': decabin_temp_value,
            'emission_ratio': trap_ratio,
            'emission_ratio_flag': emission_ratio_flag,
            'emission_flag': emission_flag,
            'trap_current_flag': trap_current_flag,
            'decabin_flag': decabin_flag}


def make_value(vs, vi):
    flag, l, h = get_flagged(vs, vi)
    if flag:
        s = '{:0.3f} ({:0.3f}-{:0.3f})'.format(vi, l, h)
    else:
        s = '{:0.2f}'.format(vi)
    return s, flag


def get_vs(tbl, n=150):
    return [v.value for v in tbl.order_by('-pub_date')[1:n]]


def get_flagged(vs, vi):
    vs = array(vs)
    avg = vs.mean()
    std = vs.std()
    l, h = avg - 2 * std, avg + 2 * std
    l, h, vi = map(lambda x: round(x, 3), (l, h, vi))
    return not (l <= vi <= h), l, h


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


seeds = string.ascii_uppercase
ALPHAS = [a for a in seeds] + ['{}{}'.format(a, b)
                               for a in seeds
                               for b in seeds]


def make_runid(a):
    identifier = a.identifier
    aliquot = a.aliquot
    increment = a.increment
    rid = '{}-{}'.format(identifier, aliquot)
    if increment is not None:
        step = ALPHAS[increment]
        rid = '{}{}'.format(rid, step)

    return rid


def make_ideogram(ans):
    ans = sorted(ans, key=lambda x: x.age)
    ages = [ai.age for ai in ans]
    age_errors = [ai.age_error for ai in ans]
    runids = [make_runid(ai) for ai in ans]

    cumulative_prob = make_cumulative_prob(ages, age_errors)
    analysis_number = make_analysis_number(ages, age_errors, runids)

    return cumulative_prob, analysis_number


def make_cumulative_prob(ages, age_errors):
    xs, ys, xmin, xmax = calculate_ideogram(ages, age_errors)
    fig = figure(tools='')
    fig.line(xs, ys)
    fig.yaxis.visible = None
    fig.logo = None
    fig.toolbar_location = None
    return _make_bokeh_components(fig)


def make_analysis_number(ages, age_errors, runids):
    hover = HoverTool()
    hover.tooltips = [('RunID', '@runids'), ('Age', '@ages')]

    ys = range(len(ages))
    source = ColumnDataSource(
        data={'ages': ages, 'ys': ys, 'runids': runids})

    fig = figure(plot_height=200, tools=[hover, ])
    fig.circle('ages', 'ys',
               source=source,
               size=5, color="navy", alpha=0.5)
    fig.xaxis.visible = None

    err_xs = []
    err_ys = []
    for x, xerr, y in zip(ages, age_errors, ys):
        err_xs.append((x - xerr, x + xerr))
        err_ys.append((y, y))

    fig.multi_line(err_xs, err_ys)
    fig.logo = None
    fig.toolbar_location = None
    return _make_bokeh_components(fig)

# def make_cumulative_prob(ages, age_errors):
#     xs, ys, xmin, xmax = calculate_ideogram(ages, age_errors)
#     xx = flot.XVariable(points=xs)
#     yy = flot.YVariable(points=ys)
#
#     series = flot.Series(x=xx, y=yy,
#                          options=flot.SeriesOptions(color='blue'))
#
#     cumulative_prob = flot.Graph(series1=series,
#                                  options=flot.GraphOptions(xaxis={'max': xmax,
#                                                                   'min': xmin},
#                                                            yaxis={'show': False}))
#     return cumulative_prob
#
#
# def make_analysis_number(ages, age_errors):
#     options = dict(points=dict(radius=2,
#                                show=True,
#                                fill=True,
#                                fillColor='blue',
#                                errorbars='x',
#                                xerr={'show': True}),
#                    color='blue')
#
#     # print xs,ys
#     data = zip(ages, age_errors)
#     data = sorted(data, key=lambda x: x[0])
#     ages, age_errors = zip(*data)
#
#     ymax = len(ages) + 1
#     ys = xrange(1, ymax)
#     xx = flot.XVariable(points=ages)
#     yy = flot.YVariable(points=ys)
#     series = flot.Series(x=xx, y=yy, options=flot.SeriesOptions(**options))
#     series['data'] = zip(ages, ys, age_errors)
#
#     analysis_number = flot.Graph(series1=series)
#     return analysis_number

# ============= EOF =============================================
