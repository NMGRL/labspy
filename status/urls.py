"""labman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from status import views, analysis_views, api_views, simple_api

router = routers.DefaultRouter()
router.register('devices', api_views.DeviceViewSet)
router.register('measurements', api_views.MeasurementViewSet)
router.register('processinfos', api_views.ProcessInfoViewSet)

urlpatterns = [
    url(r'^$', views.index, name='status_index'),
    url(r'^graph/$', views.graph, name='status_graph_index'),
    url(r'^vacuum/$', views.vacuum, name='vacuum_pressure_index'),
    url(r'^bloodtest/$', views.bloodtest, name='bloodtest_index'),
    url(r'^arar_graph/$', views.arar_graph, name='arar_graph_index'),
    url(r'^jan_status/$', views.jan_status, name='jan_status_index'),
    url(r'^felix_status/$', views.felix_status, name='felix_status_index'),
    url(r'^repository_status/$', views.repository_status, name='repository_status_index'),
    url(r'^calendar/$', views.calender, name='calendar_index'),
    url(r'^sparrow/$', views.sparrow, name='sparrow_index'),
    url(r'^all_temps/$', views.all_temps, name='all_temps_index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/analysis_count', simple_api.analysis_count, name='simple_api_index')
    # url(r'^it/$', views.it_status, name='it_index'),
    # url(r'^jan_analysis_summary', analysis_views.jan_analysis_summary, name='jan_analysis_summary'),
    # url(r'^',include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #url(r'^(?P<dr>.*)/$', views.graph_view, name='status_graph'),
    # url(r'^material/add/$', views.MaterialEntryView.as_view(), name='material_add'),
    # url(r'^material/(?P<pk>[0-9]+)/$', views.MaterialView.as_view(), name='material_detail'),
    # url(r'^sample/(?P<pk>[0-9]+)/$', views.SampleView.as_view(), name='sample_detail'),

    # url(r'^materials', views.MaterialsView.as_view(), name='materials_detail'),
    # url(r'^projects$', views.ProjectsView.as_view(), name='project_report'),
    # url(r'^api/(?P<sample_id>[\w]+)/$', views.api_detail, name='detail')
]
