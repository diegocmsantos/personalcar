from django.conf.urls.defaults import patterns, include, url

from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('views',
    ('^office/$', 'office'),
    ('^$', 'www'),
    url('^about/$', 'about', name='about'),
    url(r'^login/$', 'make_login', name='login'),
    url(r'^logout/$', logout, name='logout'),
    
    url(r'^order/', include('personalcar.order.urls')),
    url(r'^/', include('personalcar.www.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
