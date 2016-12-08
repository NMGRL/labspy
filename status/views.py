from collections import namedtuple
from datetime import datetime, timedelta

import dateutil
import requests
from dateutil import tz
from django import forms
from django.conf import settings
from django.forms import Form
from django.http import HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from status.models import Measurement, ProcessInfo, Analysis, Experiment
from status.view_helpers import make_current, connection_timestamp, make_connections, make_ideogram, \
    make_bokeh_graph, make_spectrometer_dict, get_data

DS = [{"hours": 1}, {'hours': 24}, {'weeks': 1}, {'weeks': 4}]
FMTS = ['%M:%S', '%H:%M', '%m/%d', '%m/%d']


class DateSelectorForm(Form):
    date_range_name = forms.ChoiceField(label='', choices=(('0', 'Last Hour'),
                                                           ('1', 'Last Day'),
                                                           ('2', 'Last Week'),
                                                           ('3', 'Last Month')),
                                        initial='1')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# views
def index(request):
    temps = Measurement.objects.filter(process_info__name='Lab Temp.')
    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    cfinger = Measurement.objects.filter(process_info__name='ColdFinger Temp.')
    coolant = Measurement.objects.filter(process_info__name='Coolant Temp.')
    pneumatic = Measurement.objects.filter(process_info__name='Pressure')
    pneumatic2 = Measurement.objects.filter(process_info__name='Pressure2')

    pis = ProcessInfo.objects
    temp_units = pis.get(name='Lab Temp.').units
    humidity_units = pis.get(name='Lab Hum.').units
    coolant_units = pis.get(name='Coolant Temp.').units
    coldfinger_units = pis.get(name='ColdFinger Temp.').units
    pneumatic_units = pis.get(name='Pressure').units
    pneumatic2_units = pis.get(name='Pressure').units

    cs = (('Temperature', temps, temp_units),
          ('ColdFinger', cfinger, coldfinger_units),
          ('Humidity', hums, humidity_units),
          ('Air Pressure (Building)', pneumatic, pneumatic_units),
          ('Air Pressure (Lab)', pneumatic2, pneumatic2_units),
          ('Coolant', coolant, coolant_units))
    # current = [(ti, ci.order_by('-pub_date').first().value, cu, ) for ti, ci, cu in cs]
    current = [make_current(*a) for a in cs]

    exps = []
    for tag in ('jan', 'felix'):
        exp = Experiment.objects.filter(system=tag).order_by('-start_time').first()
        an = Analysis.objects.filter(experiment=exp).order_by('-start_time').first()
        exps.append((tag, exp, an))

    connections_list = (('PyValve', connection_timestamp('pyValve'),
                         make_connections('pyValve')),
                        ('PyCO2', connection_timestamp('pyCO2'),
                         make_connections('pyCO2')))
    context = {
        'experiments': exps,
        'temp_units': temp_units,
        'humidity_units': humidity_units,
        'coolant_units': coolant_units,
        'coldfinger_units': coldfinger_units,
        'pneumatic_units': pneumatic_units,
        'events': get_org_events(latest=True),
        'connections_list': connections_list,
        'nconnections': 12 / len(connections_list),
        'current': current,
        'is_intranet': get_client_ip(request).startswith('129.138.12.')}

    return render(request, 'status/index.html', context)


def prepare_event(e):
    dt = dateutil.parser.parse(e['created_at'])
    dt = dt.astimezone(tz.tzlocal())
    e['created_at'] = dt
    return e


def get_org_events(org=None, latest=False):
    if org is None:
        org = settings.GITHUB_DATA_ORGANIZATION
    url = 'https://api.github.com/orgs/{}/events'.format(org)
    auth = {'Authorization': 'token {}'.format(settings.GITHUB_DATA_TOKEN)}
    resp = requests.get(url, headers=auth)
    events = resp.json()
    try:
        if events:
            if latest:
                events = events[:1]

            events = [prepare_event(e) for e in events]
        else:
            events = []
    except TypeError:
        events = []

    return events


def calender(request):
    context = {}
    return render(request, 'status/calendar.html', context)


def repository_status(request):
    organization_events = get_org_events()
    context = {'events': organization_events}
    return render(request, 'status/repository.html', context)


def arar_graph(request):
    latest_analysis = Analysis.objects.order_by('-start_time').first()
    identifier = latest_analysis.identifier
    ans = Analysis.objects.filter(identifier=identifier)
    cp, an = make_ideogram(ans)

    context = {'ideogram': cp,
               'analysis_number': an,
               'analyses': ans}
    return render(request, 'status/arar_graph.html', context)


def felix_status(request):
    return render_spectrometer_status(request, 'felix', 'jan')


def jan_status(request):
    return render_spectrometer_status(request, 'jan', 'felix')


def it_status(request):
    post, form = get_post(request)

    context = {'date_selector_form': form,
               'tempgraph': make_temp_graph(post, name='IT Temp.'),
               'humgraph': make_hum_graph(post, name='IT Hum.')}

    return render(request, 'status/it.html', context)


def render_spectrometer_status(request, name, oname):
    template_name = name
    cname = name.capitalize()
    oname = oname.capitalize()

    decabin_temp = Measurement.objects.filter(process_info__name='{}DecabinTemp'.format(cname))
    trap = Measurement.objects.filter(process_info__name='{}TrapCurrent'.format(cname))
    emission = Measurement.objects.filter(process_info__name='{}Emission'.format(cname))
    peakcenter = Measurement.objects.filter(process_info__name='{}PeakCenter'.format(cname))

    post, form = get_post(request)

    decabin_temp_data = get_data(decabin_temp, post)
    trap_data = get_data(trap, post)
    emission_data = get_data(emission, post)
    peakcenter_data = get_data(peakcenter, post)
    # decabin_temp_data = decabin_temp.filter(pub_date__gte=post).all()
    # trap_data = trap.filter(pub_date__gte=post).all()
    # emission_data = emission.filter(pub_date__gte=post).all()

    pis = ProcessInfo.objects
    decabin_temp_units = pis.get(name='{}DecabinTemp'.format(cname)).units

    spectrometer_values = [make_spectrometer_dict(cname),
                           make_spectrometer_dict(oname)]

    context = {'date_selector_form': form,

               'tempgraph': make_temp_graph(post),
               'decabintempgraph': make_bokeh_graph(decabin_temp_data, 'DecaBin Temperature', 'Temp ({})'.format(
                   decabin_temp_units)),
               'trapgraph': make_bokeh_graph(trap_data, 'Trap', 'uA'),
               'emissiongraph': make_bokeh_graph(emission_data, 'Emission', 'uA'),
               'peakcentergraph': make_bokeh_graph(peakcenter_data, 'PeakCenter', 'DAC (V)'),
               'spectrometer_values': spectrometer_values}

    return render(request, 'status/{}.html'.format(template_name), context)


def get_post(request):
    dt = None
    if request.method == 'POST':
        form = DateSelectorForm(request.POST)
        if form.is_valid():
            d = int(form.cleaned_data['date_range_name'])
            dt = timedelta(**DS[d])
    else:
        form = DateSelectorForm()

    if not dt:
        dt = timedelta(**DS[1])

    now = datetime.now()
    post = (now - dt)
    return post, form


def make_temp_graph(post, name='Lab Temp.', title='Temperature'):
    return make_timeseries_graph(post, name, title, 'Temp ({})')


def make_hum_graph(post, name='Lab Hum.'):
    return make_timeseries_graph(post, name, 'Humidity', 'Humidity ({})')


def make_timeseries_graph(post, name, label, unitlabel):
    pis = ProcessInfo.objects
    vs = Measurement.objects.filter(process_info__name=name)
    units = pis.get(name=name).units
    data = get_data(vs, post)
    return make_bokeh_graph(data, label, unitlabel.format(units))


def graph(request):
    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    cfinger = Measurement.objects.filter(process_info__name='ColdFinger Temp.')
    coolant = Measurement.objects.filter(process_info__name='Coolant Temp.')
    pneumatic = Measurement.objects.filter(process_info__name='Pressure')
    pneumatic2 = Measurement.objects.filter(process_info__name='Pressure2')

    pis = ProcessInfo.objects
    humidity_units = pis.get(name='Lab Hum.').units
    coolant_units = pis.get(name='Coolant Temp.').units
    coldfinger_units = pis.get(name='ColdFinger Temp.').units
    pneumatic_units = pis.get(name='Pressure').units
    pneumatic2_units = pis.get(name='Pressure2').units

    post, form = get_post(request)

    context = {'date_selector_form': form,
               'tempgraph': make_temp_graph(post)}

    s = (('humgraph', hums, 'Humidity', 'Humidity ({})'.format(humidity_units)),
         ('pneugraph', pneumatic, 'Pneumatics (Lab)', 'Pressure ({})'.format(pneumatic_units)),
         ('pneugraph2', pneumatic2, 'Pneumatics (Building)', 'Pressure ({})'.format(pneumatic2_units)),
         ('coolgraph', coolant, 'Coolant', 'Temp ({})'.format(coolant_units)),
         ('cfgraph', cfinger, 'ColdFinger', 'Temp ({})'.format(coldfinger_units)))
    for key, table, title, ytitle in s:
        context[key] = make_bokeh_graph(get_data(table, post), title, ytitle)

    return render(request, 'status/graph.html', context)


def all_temps(request):
    post, form = get_post(request)

    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    humidity_units = ProcessInfo.objects.get(name='Lab Hum.').units

    hums2 = Measurement.objects.filter(process_info__name='Lab Hum. 2')
    humidity_units2 = ProcessInfo.objects.get(name='Lab Hum. 2').units

    context = {'tempgraph': make_temp_graph(post),
               'humgraph': make_bokeh_graph(get_data(hums, post), 'Humidity', 'Humidity ({})'.format(humidity_units)),
               'sensehat_hum': make_bokeh_graph(get_data(hums2, post),
                                                'Humidity 2', 'Humidity ({})'.format(humidity_units2)),
               'date_selector_form': form}

    for tag, name, title in (('sensehat_temp1', 'Lab Temp. 2', 'Sensehat Temp1'),
                             ('tprobe_temp3', 'Lab Temp. 3', 'TProbe Temp3'),
                             ('tprobe_temp4', 'Lab Temp. 4', 'TProbe Temp4'),
                             ('tprobe_temp5', 'Lab Temp. 5', 'TProbe Temp5'),
                             ('tprobe_temp6', 'Lab Temp. 6', 'TProbe Temp6')):
        context[tag] = make_temp_graph(post, name=name, title=title)

    return render(request, 'status/all_temps.html', context)
