from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('order',
    # client
    (r'^add_client/$', 'views.add_client'),
    (r'^list_client/$', 'views.list_client'),
    
    # order
    (r'^add_order/(?P<client_id>\d+)/$', 'views.add_order'),
    (r'^list_order/$', 'views.list_order'),
    (r'^order/(?P<id>\d+)/$', 'views.order'),
    
    # Service
    (r'^add_service/$', 'views.add_service'),
    (r'^list_service/$', 'views.list_service'),
    (r'^list_service_json/$', 'views.list_service_json'),
    
    # Part
    (r'^add_part/$', 'views.add_part'),
    (r'^list_part/$', 'views.list_part'),
    (r'^list_parts_by_ids/(?P<list_parts_id>\w+)/$', 'views.list_part_json'),
    
    (r'^list_service_json/$', 'views.list_service_json'),
)
