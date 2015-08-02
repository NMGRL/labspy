from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django_tables2 import Table, RequestConfig
from samples.forms import MaterialForm, SampleForm, ProjectForm, AssignmentForm, SamplePrepForm
from samples.models import Material, Project, Sample, SamplePrep, Assignment


def index(request):
    ctx = {}
    return render(request, 'samples/map.html', ctx)

#
# class MaterialTable(Table):
#     class Meta:
#         model = Material
#         attrs = {'class': 'paleblue'}
#
#
# class ProjectTable(Table):
#     class Meta:
#         model = Project
#         attrs = {'class': 'paleblue'}
#
#
# class SampleTable(Table):
#     class Meta:
#         model = Sample
#         attrs = {'class': 'paleblue'}
#
#
# def index(request):
#     materials = MaterialTable(Material.objects.all())
#     RequestConfig(request).configure(materials)
#
#     projects = ProjectTable(Project.objects.all())
#     RequestConfig(request).configure(projects)
#
#     samples = SampleTable(Sample.objects.all())
#     RequestConfig(request).configure(samples)
#
#     return render(request, 'samples/index.html',
#                   {'materials': materials,
#                    'projects': projects,
#                    'samples': samples})
#
#
# def material_add(request):
#     if request.method == 'POST':
#         form = MaterialForm(request.POST)
#         if form.is_valid():
#             # print 'ffff',form.cleaned_data['name']
#             form.save()
#             # print 'request', request.GET.items()#['name']
#             # Material.objects.create(name=request.get('name'))
#
#             return HttpResponse('thanks')
#     else:
#         form = MaterialForm()
#     return render(request, 'samples/material_form.html', {'form': form})
#
#
# def sample_add(request):
#     if request.method == 'POST':
#         form = SampleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('thanks')
#     else:
#         form = SampleForm()
#     return render(request, 'samples/sample_form.html', {'form': form})
#
#
# def project_add(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('thanks')
#     else:
#         form = ProjectForm()
#     return render(request, 'samples/project_form.html', {'form': form})
#
#
# def sample_image_add(request):
#     return HttpResponse('Sample Image Add not enabled')
#
#
# def assignment(request):
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             sample = form.cleaned_data['sample']
#             SamplePrep.objects.create(sample=sample)
#
#             return HttpResponse('thanks')
#     else:
#         form = AssignmentForm()
#
#     return render(request, 'samples/assignment_form.html', {'form': form})
#
#
# def sample_prep(request, pk):
#     if pk:
#         if request.method == 'POST':
#             instance = SamplePrep.objects.get(pk=pk)
#             form = SamplePrepForm(request.POST, instance=instance)
#             if form.is_valid():
#                 form.save()
#
#                 # sample = form.cleaned_data['sample']
#                 # SamplePrep.objects.create(sample=sample)
#
#                 # return HttpResponse('thanks')
#         else:
#             instance = SamplePrep.objects.get(pk=pk)
#             form = SamplePrepForm(instance=instance)
#     else:
#         return HttpResponse('no prep')
#
#     return render(request, 'samples/sample_prep_form.html',
#                   {'form': form,
#                    'prep': instance})
#
#
# def worker_sample_prep(request, username):
#     if request.method == 'POST':
#         instance = Assignment.objects.get(worker__username=username)
#         samples = []
#         # form = SamplePrepList(instance=instance)
#         # form = SamplePrepForm(request.POST, instance=instance)
#         # if form.is_valid():
#         #     form.save()
#
#             # sample = form.cleaned_data['sample']
#             # SamplePrep.objects.create(sample=sample)
#
#             # return HttpResponse('thanks')
#     else:
#         samples = Assignment.objects.filter(worker__username=username).all()
#         # form = SamplePrepList(instance=instance)
#
#     return render(request, 'samples/worker_sample_prep.html', {'samples': samples})
#
#
# # report views
# class MaterialsView(generic.ListView):
#     # model = Material
#     template_name = 'samples/material_report.html'
#     context_object_name = 'materials'
#
#     def get_queryset(self):
#         return Material.objects.all()
#
#
# class ProjectsView(generic.ListView):
#     # model = Material
#     template_name = 'samples/project_report.html'
#     context_object_name = 'projects'
#
#     def get_queryset(self):
#         return Project.objects.all()
#
#
# class MaterialView(generic.DetailView):
#     model = Material
#     template_name = 'samples/material_detail.html'
#
#
# class SampleView(generic.DetailView):
#     model = Sample
#     template_name = 'samples/sample_detail.html'
#
#
# class MaterialEntryView(generic.edit.CreateView):
#     model = Material
#     fields = ['name']
#
#
# class SampleCreateView(generic.edit.CreateView):
#     model = Sample
#     fields = ['name', 'material', 'project']
