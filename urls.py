from django.conf.urls.defaults import patterns, include, url

from django.views.generic.simple import direct_to_template
from django.contrib.auth import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^order/', include('personalcar.order.urls')),
    
    url('^about/$', 'views.about', name='about'),
    ('^$', direct_to_template, {'template': 'index.html'}),
    url(r'^login/$', 'views.make_login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    # Examples:
    # url(r'^$', 'personalcat.views.home', name='home'),
    # url(r'^personalcat/', include('personalcat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
