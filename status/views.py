from datetime import datetime, timedelta
from django import forms
from django.forms import Form
from django.shortcuts import render
import flot
# Create your views here.
from status.models import Measurement

DS = [{"hours": 1}, {'hours': 24}, {'weeks': 1}, {'weeks': 4}]
FMTS = ['%M:%S', '%H:%M', '%m/%d', '%m/%d']


class DateSelectorForm(Form):
    date_range_name = forms.ChoiceField(label='', choices=((0, 'Last Hour'),
                                                           (1, 'Last Day'),
                                                           (2, 'Last Week'),
                                                           (3, 'Last Month')))


def index(request):
    temps = Measurement.objects.filter(process_info__name='temp')
    hums = Measurement.objects.filter(process_info__name='humidity')
    temp_data = None
    hum_data = None
    fmt = '%H:%M:%S'
    if request.method == 'POST':
        form = DateSelectorForm(request.POST)
        if form.is_valid():
            d = int(form.cleaned_data['date_range_name'])
            now = datetime.now()
            post = now - timedelta(**DS[d])
            temp_data = temps.filter(pub_date__gte=post).all()
            hum_data = hums.filter(pub_date__gte=post).all()
            # tdata = [(i, m.value) for i, m in enumerate(temps.filter(pub_date__gte=post).all())]
            # hdata = [(i, m.value) for i, m in enumerate(temps.filter(pub_date__gte=post).all())]
            fmt = FMTS[d]
    else:
        form = DateSelectorForm()
        hum_data = hums.all()
        temp_data = temps.all()
        # temp_data = [(m.pub_date, m.value) for i, m in enumerate(temps.all())]

    if not temp_data:
        temp_xs = [0]
        temp_ys = [0]
    else:
        temp_xs, temp_ys = zip(*[(m.pub_date, m.value) for m in temp_data])

    if not hum_data:
        hum_xs = [0]
        hum_ys = [0]
    else:
        hum_xs, hum_ys = zip(*[(m.pub_date, m.value) for m in hum_data])

    series = flot.Series(x=flot.TimeXVariable(points=temp_xs),
                         y=flot.YVariable(points=temp_ys),
                         options=flot.SeriesOptions(color='red'))
    temp = flot.Graph(series1=series,
                      options=flot.GraphOptions(xaxis={'mode': 'time', 'timeformat': fmt}))

    series1 = flot.Series(x=flot.TimeXVariable(points=hum_xs),
                         y=flot.YVariable(points=hum_ys),
                         options=flot.SeriesOptions(color='red'))
    hum = flot.Graph(series1=series1,
                     options=flot.GraphOptions(xaxis={'mode': 'time', 'timeformat': fmt}))

    context = {'temp': temp,
               'hum': hum,
               'date_selector_form': form}
    return render(request, 'status/index.html', context)
