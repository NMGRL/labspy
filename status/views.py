from collections import namedtuple
from datetime import datetime, timedelta

import dateutil
import requests
from dateutil import tz
from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from numpy import array

from status.models import Measurement, ProcessInfo, Analysis, Experiment
from status.view_helpers import make_current, connection_timestamp, make_connections, make_ideogram, \
    make_bokeh_graph, make_spectrometer_dict, get_data, get_post, get_client_ip, calc_bloodtest


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


def bloodtest(request):
    now = datetime.now()
    post = now - timedelta(weeks=400)
    context = {}
    bs = []
    for name, piname in (('Lab Temp.', 'Lab Temp.'),
                         ('Lab Hum.', 'Lab Hum.'),
                         ('Lab Pressure', 'Pressure'),
                         ('Building Pressure', 'Pressure2'),
                         ('Coolant Temp.', 'Coolant Temp.'),
                         ('ColdFinger Temp.', 'ColdFinger Temp.'),
                         ('BoneIonGauge', 'BoneIonGauge'),
                         ('MicroBoneIonGauge', 'MicroBoneIonGauge'),
                         ('RoughingIonGauge', 'RoughingIonGauge'),):
        table = Measurement.objects.filter(process_info__name=piname)
        data = table.filter(pub_date__gte=post).all()

        bt = calc_bloodtest(name, data)
        bs.append(bt)

    context['bloodtests'] = bs
    return render(request, 'status/bloodtest.html', context)


def make_temp_graph(post, name='Lab Temp.', title='Temperature'):
    return make_timeseries_graph(post, name, title, 'Temp ({})')


def make_hum_graph(post, name='Lab Hum.'):
    return make_timeseries_graph(post, name, 'Humidity', 'Humidity ({})')


def make_timeseries_graph(post, name, label, unitlabel):
    pis = ProcessInfo.objects
    vs = Measurement.objects.filter(process_info__name=name)
    units = pis.get(name=name).units

    if label is None:
        label = pis.get(name=name).graph_title

    data = get_data(vs, post)
    return make_bokeh_graph(data, label, unitlabel.format(units))


def graph(request):
    post, form = get_post(request)

    context = {'date_selector_form': form,
               'temp': make_temp_graph(post)}
    for ctxkey, piname in (('hum', 'Lab Hum.'),
                           ('pneu', 'Pressure'),
                           ('pneu2', 'Pressure2'),
                           ('coolant', 'Coolant Temp.'),
                           ('coldfinger', 'ColdFinger Temp.')):
        data = Measurement.objects.filter(process_info__name=piname)
        pi = ProcessInfo.objects.get(name=piname)
        context[ctxkey] = make_bokeh_graph(get_data(data, post), pi.graph_title, pi.ytitle)

    return render(request, 'status/graph.html', context)


def all_temps(request):
    post, form = get_post(request)

    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    pos = ProcessInfo.objects
    hum = pos.get(name='Lab Hum.')
    humidity_units = hum.units

    hums2 = Measurement.objects.filter(process_info__name='Lab Hum. 2')
    hum2 = ProcessInfo.objects.get(name='Lab Hum. 2')

    context = {'tempgraph': make_temp_graph(post, title=None),
               'humgraph': make_bokeh_graph(get_data(hums, post), hum.graph_title, 'Humidity ({})'.format(
                   humidity_units)),
               'sensehat_hum': make_bokeh_graph(get_data(hums2, post),
                                                hum2.graph_title, 'Humidity ({})'.format(hum2.units)),
               'date_selector_form': form}

    for tag, name in (('sensehat_temp1', 'Lab Temp. 2'),
                      ('tprobe_temp3', 'Lab Temp. 3'),
                      ('tprobe_temp4', 'Lab Temp. 4'),
                      ('tprobe_temp5', 'Lab Temp. 5'),
                      ('tprobe_temp6', 'Lab Temp. 6'),
                      ('tprobe_temp7', 'Lab Temp. 7'),
                      ('noaa_temp', 'Outside Temp'),
                      ):
        obj = pos.get(name=name)
        context[tag] = make_temp_graph(post, name=name, title=obj.graph_title)

    return render(request, 'status/all_temps.html', context)


def vacuum(request):
    post, form = get_post(request)

    context = {'date_selector_form': form}
    ytitle = 'Pressure (torr)'
    bs = []
    for ctxkey, pikey in (('big', 'BoneIonGauge'),
                          ('mbig', 'MicroBoneIonGauge'),
                          ('rig', 'RoughingIonGauge'),

                          ('btank', 'BoneTank'),
                          ('mbtank', 'MicroBoneTank'),
                          ('rtank', 'RoughingTank'),

                          ('ascroll', 'AnalyticalScroll'),
                          ('rscroll', 'RoughingScroll'),
                          ('jdb', 'JanDecabinPressure'),

                          ('fig', 'FirstStageIonGauge'),
                          ('fsd', 'FirstStageDiaphram'),
                          ('fud', 'FurnaceDiaphram')):
        obj = Measurement.objects.filter(process_info__name=pikey)
        po = ProcessInfo.objects.get(name=pikey)
        data = get_data(obj, post)
        context[ctxkey] = make_bokeh_graph(data, po.graph_title, ytitle)

        bt = calc_bloodtest(pikey, data)
        bs.append(bt)

    context['bloodtests'] = bs

    return render(request, 'status/vacuum.html', context)
