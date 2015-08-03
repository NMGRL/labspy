from datetime import datetime, timedelta
from django import forms
from django.forms import Form
from django.shortcuts import render
import flot
# Create your views here.
from status.models import Measurement, ProcessInfo, Analysis, Experiment

DS = [{"hours": 1}, {'hours': 24}, {'weeks': 1}, {'weeks': 4}]
FMTS = ['%M:%S', '%H:%M', '%m/%d', '%m/%d']


class DateSelectorForm(Form):
    date_range_name = forms.ChoiceField(label='', choices=((0, 'Last Hour'),
                                                           (1, 'Last Day'),
                                                           (2, 'Last Week'),
                                                           (3, 'Last Month')))


def index(request):
    temps = Measurement.objects.filter(process_info__name='Lab Temp.')
    hums = Measurement.objects.filter(process_info__name='Lab Hum.')
    cfinger = Measurement.objects.filter(process_info__name='ColdFinger Temp.')
    coolant = Measurement.objects.filter(process_info__name='Coolant Temp.')
    pneumatic = Measurement.objects.filter(process_info__name='Pressure')

    temp_data = None
    hum_data = None
    fmt = '%H:%M:%S'
    pis = ProcessInfo.objects
    temp_units = pis.get(name='Lab Temp.').units
    humidity_units = pis.get(name='Lab Hum.').units
    coolant_units = pis.get(name='Coolant Temp.').units
    coldfinger_units = pis.get(name='ColdFinger Temp.').units
    pneumatic_units = pis.get(name='Pressure').units

    current_temp = temps.order_by('-pub_date').first().value
    current_hum = hums.order_by('-pub_date').first().value

    jan_tag = 'jan'
    ob_tag = 'obama'

    cur_jan_exp = Experiment.objects.filter(system=jan_tag).order_by('-start_time').first()
    cur_ob_exp = Experiment.objects.filter(system=ob_tag).order_by('-start_time').first()

    cur_jan_an = Analysis.objects.filter(experiment=cur_jan_exp).order_by('-start_time').first()
    cur_ob_an = Analysis.objects.filter(experiment=cur_ob_exp).order_by('-start_time').first()

    if request.method == 'POST':
        form = DateSelectorForm(request.POST)
        if form.is_valid():
            d = int(form.cleaned_data['date_range_name'])
            now = datetime.now()
            post = now - timedelta(**DS[d])
            temp_data = temps.filter(pub_date__gte=post).all()
            hum_data = hums.filter(pub_date__gte=post).all()
            cf_data = cfinger.filter(pub_date__gte=post).all()
            cool_data = coolant.filter(pub_date__gte=post).all()
            pneumatic_data = pneumatic.filter(pub_date__gte=post).all()

            fmt = FMTS[d]
    else:
        form = DateSelectorForm()
        hum_data = hums.all()
        temp_data = temps.all()
        cf_data = cfinger.all()
        cool_data = coolant.all()
        pneumatic_data = pneumatic.all()

    context = {'temp': make_graph(temp_data, fmt),
               'hum': make_graph(hum_data, fmt),
               'cfinger': make_graph(cf_data, fmt),
               'coolant': make_graph(cool_data, fmt),
               'pneumatic': make_graph(pneumatic_data, fmt),
               'experiments': [(jan_tag, cur_jan_exp,
                                cur_jan_an),
                               (ob_tag, cur_ob_exp,
                                cur_ob_an)],
               'temp_units': temp_units,
               'humidity_units': humidity_units,
               'coolant_units': coolant_units,
               'coldfinger_units': coldfinger_units,
               'pneumatic_units': pneumatic_units,
               'current_temp': current_temp,
               'current_humidity': current_hum,
               'date_selector_form': form}
    return render(request, 'status/index.html', context)


def make_graph(data, fmt=None):
    # print data
    if not fmt:
        fmt = '%H:%M:%S'

    yklass = flot.YVariable
    if data:
        xs, ys = zip(*[(m.pub_date, m.value) for m in data])
        xklass = flot.TimeXVariable
    else:
        xs, ys = [], []
        xklass = flot.XVariable

    # print xs,ys
    series1 = flot.Series(x=xklass(points=xs),
                          y=yklass(points=ys),
                          options=flot.SeriesOptions(color='red'))
    graph = flot.Graph(series1=series1,
                       options=flot.GraphOptions(xaxis={'mode': 'time', 'timeformat': fmt}))
    return graph
