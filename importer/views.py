import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic import CreateView
from importer.models import ImportRequest


class ImportRequestForm(forms.Form):
    requestor_name = forms.CharField(label='Name')
    experiment_identifier = forms.CharField(label='Experiment Identifier')
    is_irradiation = forms.BooleanField(label='Is Irradiation', required=False)
    runlist_blob = forms.FileField(label='Analysis List', required=True)

    def __init__(self, *args, **kwargs):
        super(ImportRequestForm, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_class = 'form-horizontal'

        # helper.label_class = 'col-lg-2'
        # helper.field_class = 'col-lg-8'
        # helper.field_template = 'bootstrap/layout/inline_field.html'
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'blueForms'
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'submit_survey'
        helper.add_input(Submit('check_runlist', 'Check Run List'))
        helper.add_input(Submit('submit_request', 'Submit Request'))
        self.helper = helper


def import_request_result(request):
    raise Http404('Not implemented')


def file_to_blob(rf):
    txt = ''.join(rf.chunks())
    return txt


regex = re.compile(r'^(?P<runid>(\d+-\d{2}\w{0,2}$)|(\w{1,2}-(\d|\w){2}-\w*-\d*)$)')


def validate_runlist(request):
    rfile = request.FILES['runlist_blob']
    blob = file_to_blob(rfile)

    error = None
    runlist = []
    elist = []
    for i, line in enumerate(blob.split('\n')):
        m = regex.match(line)
        if m:
            runlist.append(m.group('runid'))
        else:
            if line.strip():
                elist.append((i, line))

    return '\n'.join(runlist), runlist, elist, error


def index(request):
    runlist_error = None
    runlist = None
    elist = None
    if request.method == 'POST':
        form = ImportRequestForm(request.POST, request.FILES)
        # print request.POST
        # print 'ff', form.data
        if 'check_runlist' in form.data:
            blob, runlist, elist, runlist_error = validate_runlist(request)

        elif form.is_valid():
            p = request.POST
            blob, runlist, elist, runlist_error = validate_runlist(request)
            if blob:
                ImportRequest.objects.create(experiment_identifier=p.get('experiment_identifier'),
                                             runlist_blob=blob,
                                             request_date=timezone.now(),
                                             requestor_name=p.get('requestor_name'))
    else:
        form = ImportRequestForm()

    imported = ImportRequest.objects.exclude(imported_date__isnull=True)
    to_import = ImportRequest.objects.exclude(imported_date__isnull=False)

    ctx = {'request_form': form,
           'imported_requests': imported,
           'to_import_requests': to_import,
           'runlist_error': runlist_error,
           'alist': runlist, 'elist': elist}
    return render(request, 'importer/index.html', ctx)
