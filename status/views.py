from datetime import datetime, timedelta
from django import forms
from django.forms import Form
from django.http import Http404
from django.shortcuts import render
# from django.utils import timezone
import flot
import time

# Create your views here.
from status.models import Measurement, ProcessInfo, Analysis, Experiment, Connections

DS = [{"hours": 1}, {'hours': 24}, {'weeks': 1}, {'weeks': 4}]
FMTS = ['%M:%S', '%H:%M', '%m/%d', '%m/%d']


class DateSelectorForm(Form):
    date_range_name = forms.ChoiceField(label='', choices=(('0', 'Last Hour'),
                                                           ('1', 'Last Day'),
                                                           ('2', 'Last Week'),
                                                           ('3', 'Last Month')),
                                        initial='1')


class SaveFigureForm(Form):
    pass


def make_current(ti, di, ui):
    obj = di.order_by('-pub_date').first()
    return ti, obj.value, ui, obj.pub_date


def make_connections(name):
    return Connections.objects.filter(appname=name).values()


def connection_timestamp(name):
    f = Connections.objects.filter(appname=name).first()
    if f:
        return f.timestamp


def index(request):
    temps = Measurement.objects.filter(process_info__name='Lab Temp.')
    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    cfinger = Measurement.objects.filter(process_info__name='ColdFinger Temp.')
    coolant = Measurement.objects.filter(process_info__name='Coolant Temp.')
    pneumatic = Measurement.objects.filter(process_info__name='Pressure')

    pis = ProcessInfo.objects
    temp_units = pis.get(name='Lab Temp.').units
    humidity_units = pis.get(name='Lab Hum.').units
    coolant_units = pis.get(name='Coolant Temp.').units
    coldfinger_units = pis.get(name='ColdFinger Temp.').units
    pneumatic_units = pis.get(name='Pressure').units

    cs = (('Temperature', temps, temp_units),
          ('ColdFinger', cfinger, coldfinger_units),
          ('Humidity', hums, humidity_units),
          ('Air Pressure', pneumatic, pneumatic_units),
          ('Coolant', coolant, coolant_units))
    # current = [(ti, ci.order_by('-pub_date').first().value, cu, ) for ti, ci, cu in cs]
    current = [make_current(*a) for a in cs]
    jan_tag = 'jan'
    ob_tag = 'obama'

    cur_jan_exp = Experiment.objects.filter(system=jan_tag).order_by('-start_time').first()
    cur_ob_exp = Experiment.objects.filter(system=ob_tag).order_by('-start_time').first()

    cur_jan_an = Analysis.objects.filter(experiment=cur_jan_exp).order_by('-start_time').first()
    cur_ob_an = Analysis.objects.filter(experiment=cur_ob_exp).order_by('-start_time').first()

    connections_list = (('PyValve', connection_timestamp('pyValve'),
                         make_connections('pyValve')),
                        ('PyCO2', connection_timestamp('pyCO2'),
                         make_connections('pyCO2')))
    context = {
        'experiments': [(jan_tag, cur_jan_exp,
                         cur_jan_an),
                        (ob_tag, cur_ob_exp,
                         cur_ob_an)],
        'temp_units': temp_units,
        'humidity_units': humidity_units,
        'coolant_units': coolant_units,
        'coldfinger_units': coldfinger_units,
        'pneumatic_units': pneumatic_units,

        'connections_list': connections_list,
        'nconnections': 12 / len(connections_list),
        'current': current}
    return render(request, 'status/index.html', context)


def arar_graph(request):
    latest_analysis = Analysis.objects.order_by('-start_time').first()
    identifier = latest_analysis.identifier
    ans = Analysis.objects.filter(identifier=identifier)
    cp, an = make_ideogram(ans)
    context = {'cumulative_prob': cp,
               'analysis_number': an,
               'analyses': ans}
    return render(request, 'status/arar_graph.html', context)


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

    cumulative_prob= make_cumulative_prob(ages, age_errors)
    analysis_number = make_analysis_number(ages, age_errors)

    return cumulative_prob, analysis_number


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

    ymax = len(ages)+1
    ys = xrange(1, ymax)
    xx = flot.XVariable(points=ages)
    yy = flot.YVariable(points=ys)
    series = flot.Series(x=xx, y=yy, options=flot.SeriesOptions(**options))
    series['data'] = zip(ages, ys, age_errors)

    analysis_number = flot.Graph(series1=series)
    return analysis_number


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


def graph(request):
    temps = Measurement.objects.filter(process_info__name='Lab Temp.')
    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    cfinger = Measurement.objects.filter(process_info__name='ColdFinger Temp.')
    coolant = Measurement.objects.filter(process_info__name='Coolant Temp.')
    pneumatic = Measurement.objects.filter(process_info__name='Pressure')

    fmt = '%H:%M:%S'
    pis = ProcessInfo.objects
    temp_units = pis.get(name='Lab Temp.').units
    humidity_units = pis.get(name='Lab Hum.').units
    coolant_units = pis.get(name='Coolant Temp.').units
    coldfinger_units = pis.get(name='ColdFinger Temp.').units
    pneumatic_units = pis.get(name='Pressure').units

    dt = None
    if request.method == 'POST':

        fig_form = SaveFigureForm(request.POST)
        form = DateSelectorForm(request.POST)

        if form.is_valid():
            d = int(form.cleaned_data['date_range_name'])
            dt = timedelta(**DS[d])
            fmt = FMTS[d]

    else:
        fig_form = SaveFigureForm()
        form = DateSelectorForm()

    if not dt:
        dt = timedelta(**DS[1])

    now = datetime.now()
    post = (now - dt)

    temp_data = temps.filter(pub_date__gte=post).all()
    hum_data = hums.filter(pub_date__gte=post).all()
    cf_data = cfinger.filter(pub_date__gte=post).all()
    cool_data = coolant.filter(pub_date__gte=post).all()
    pneumatic_data = pneumatic.filter(pub_date__gte=post).all()

    temp = make_graph(temp_data, fmt)
    hum = make_graph(hum_data, fmt)
    cfinger = make_graph(cf_data, fmt)
    coolant = make_graph(cool_data, fmt)
    pneumatic = make_graph(pneumatic_data, fmt)

    row1 = (('Temperature', 'Temp ({})'.format(temp_units), 'temp_graph', temp),
            ('Humidity', 'Humidity ({})'.format(humidity_units), 'hum_graph', hum))
    row2 = (('ColdFinger', 'Temp ({})'.format(coldfinger_units), 'cf_graph', cfinger),
            ('Pneumatics', 'Pressure ({})'.format(pneumatic_units), 'pn_graph', pneumatic))
    row3 = (('Coolant', 'Temp ({})'.format(coolant_units), 'coolant_graph', coolant),)

    context = {
        'graphrows': (row1, row2, row3),
        'temp_units': temp_units,
        'humidity_units': humidity_units,
        'coolant_units': coolant_units,
        'coldfinger_units': coldfinger_units,
        'pneumatic_units': pneumatic_units,

        'save_figure_form': fig_form,
        'date_selector_form': form}
    return render(request, 'status/graph.html', context)


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
