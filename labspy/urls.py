"""labman URL Configuration

The `urlpatterns` list routes URLs to views. For more infsaormation please see:
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
from labspy.views import Home, People, Hardware, Software, SoftwareMassSpec, SoftwarePychron
from status import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', Home.as_view(), name='home'),
    # url(r'^people$', People.as_view(), name='people'),
    url(r'^$', views.index, name='status_index'),
    url(r'^hardware$', Hardware.as_view(), name='hardware'),
    url(r'^software$', Software.as_view(), name='software'),
    url(r'^software/massspec$', SoftwareMassSpec.as_view(), name='software_massspec'),
    url(r'^software/pychron$', SoftwarePychron.as_view(), name='software_pychron'),
    url(r'^/labspy/status/', include('status.urls')),
    url(r'^mples/', include('samples.urls')),
    url(r'^importer/', include('importer.urls')),

]
