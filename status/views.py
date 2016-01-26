from datetime import datetime, timedelta
from django import forms
from django.forms import Form
from django.shortcuts import render

# Create your views here.
from status.models import Measurement, ProcessInfo, Analysis, Experiment
from status.view_helpers import make_current, connection_timestamp, make_connections, make_ideogram, \
    make_bokeh_graph, make_spectrometer_dict

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
    context = {'cumulative_prob': cp,
               'analysis_number': an,
               'analyses': ans}
    return render(request, 'status/arar_graph.html', context)


def graph(request):
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
    pneumatic2_units = pis.get(name='Pressure2').units

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

    temp_data = temps.filter(pub_date__gte=post).all()
    hum_data = hums.filter(pub_date__gte=post).all()
    cf_data = cfinger.filter(pub_date__gte=post).all()
    cool_data = coolant.filter(pub_date__gte=post).all()
    pneumatic_data = pneumatic.filter(pub_date__gte=post).all()
    pneumatic2_data = pneumatic2.filter(pub_date__gte=post).all()

    spectrometer_values = [make_spectrometer_dict('Jan'),
                           make_spectrometer_dict('Obama+')]

    context = {
        'date_selector_form': form,

        'tempgraph': make_bokeh_graph(temp_data, 'Temperature', 'Temp ({})'.format(temp_units)),
        'humgraph': make_bokeh_graph(hum_data, 'Humidity', 'Humidity ({})'.format(humidity_units)),
        'pneugraph': make_bokeh_graph(pneumatic_data, 'Pneumatics (Lab)',
                                      'Pressure ({})'.format(pneumatic_units)),
        'pneugraph2': make_bokeh_graph(pneumatic2_data, 'Pneumatics (Building)',
                                       'Pressure ({})'.format(pneumatic2_units)),
        'coolgraph': make_bokeh_graph(cool_data, 'Coolant', 'Temp ({})'.format(coolant_units)),
        'cfgraph': make_bokeh_graph(cf_data, 'ColdFinger', 'Temp ({})'.format(coldfinger_units)),

        'spectrometer_values': spectrometer_values}
    return render(request, 'status/graph.html', context)
