from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('admin.controllers.account',

    #url(r'^$'), ''),

    # Examples:
    # url(r'^$', 'anou.views.home', name='home'),
    # url(r'^projectomar/', include('projectomar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
