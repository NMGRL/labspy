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
from samples import views

urlpatterns = [
    url(r'^$', views.index, name='sample_index'),

    # url(r'^material/add/$', views.material_add, name='material_add'),
    # url(r'^sample/add/$', views.sample_add, name='sample_add'),
    # url(r'^project/add/$', views.project_add, name='project_add'),
    # url(r'^image/add/$', views.sample_image_add, name='sample_image_add'),
    #
    # url(r'^assignment/add/$', views.assignment, name='assignment'),
    # url(r'^prep/(?P<username>.*)/$', views.worker_sample_prep, name='worker_sample_prep'),
    # url(r'^prep/(?P<pk>[0-9]*)/$', views.sample_prep, name='sampleprep'),

    # url(r'^sampleprep/$', views.sample_prep, name='sample_prep'),

    # url(r'^material/(?P<pk>[0-9]+)/$', views.MaterialView.as_view(), name='material_detail'),
    # url(r'^sample/(?P<pk>[0-9]+)/$', views.SampleView.as_view(), name='sample_detail'),

    # url(r'^materials', views.MaterialsView.as_view(), name='materials_detail'),
    # url(r'^projects$', views.ProjectsView.as_view(), name='project_report'),
    # url(r'^api/(?P<sample_id>[\w]+)/$', views.api_detail, name='detail')
]
