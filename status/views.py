from collections import namedtuple
from datetime import datetime, timedelta
from django import forms
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

    context = {'ideogram': cp,
               'analysis_number': an,
               'analyses': ans,
               }
    return render(request, 'status/arar_graph.html', context)


def obama_status(request):
    return render_spectrometer_status(request, 'obama', 'jan')


def jan_status(request):
    return render_spectrometer_status(request, 'jan', 'obama')


def render_spectrometer_status(request, name, oname):
    template_name = name
    cname = name.capitalize()
    oname = oname.capitalize()

    decabin_temp = Measurement.objects.filter(process_info__name='{}DecabinTemp'.format(cname))
    trap = Measurement.objects.filter(process_info__name='{}TrapCurrent'.format(cname))
    emission = Measurement.objects.filter(process_info__name='{}Emission'.format(cname))

    post, form = get_post(request)

    decabin_temp_data = get_data(decabin_temp, post)
    trap_data = get_data(trap, post)
    emission_data = get_data(emission, post)

    # decabin_temp_data = decabin_temp.filter(pub_date__gte=post).all()
    # trap_data = trap.filter(pub_date__gte=post).all()
    # emission_data = emission.filter(pub_date__gte=post).all()

    pis = ProcessInfo.objects
    decabin_temp_units = pis.get(name='{}DecabinTemp'.format(cname)).units

    spectrometer_values = [make_spectrometer_dict(cname),
                           make_spectrometer_dict(oname)]

    context = {'date_selector_form': form,

               'tempgraph': make_lab_temp_graph(post),
               'decabintempgraph': make_bokeh_graph(decabin_temp_data, 'DecaBin Temperature', 'Temp ({})'.format(
                   decabin_temp_units)),
               'trapgraph': make_bokeh_graph(trap_data, 'Trap', 'uA'),
               'emissiongraph': make_bokeh_graph(emission_data, 'Emission', 'uA'),
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


def make_lab_temp_graph(post):
    pis = ProcessInfo.objects
    temps = Measurement.objects.filter(process_info__name='Lab Temp.')
    temp_units = pis.get(name='Lab Temp.').units
    temp_data = get_data(temps, post)
    return make_bokeh_graph(temp_data, 'Temperature', 'Temp ({})'.format(temp_units))


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
               'tempgraph': make_lab_temp_graph(post)}

    s = (('humgraph', hums, 'Humidity', 'Humidity ({})'.format(humidity_units)),
         ('pneugraph', pneumatic, 'Pneumatics (Lab)', 'Pressure ({})'.format(pneumatic_units)),
         ('pneugraph2', pneumatic2, 'Pneumatics (Building)', 'Pressure ({})'.format(pneumatic2_units)),
         ('coolgraph', coolant, 'Coolant', 'Temp ({})'.format(coolant_units)),
         ('cfgraph', cfinger, 'ColdFinger', 'Temp ({})'.format(coldfinger_units)))
    for key, table, title, ytitle in s:
        context[key] = make_bokeh_graph(get_data(table, post), title, ytitle)

    return render(request, 'status/graph.html', context)
