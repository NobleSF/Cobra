from django.conf.urls import patterns, include, url
from public.controller import home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', home.home, name='home'), # fyi, this is home
)

urlpatterns += patterns('',
  url(r'^', include('public.urls')),
  url(r'^account/', include('admin.urls')),
  url(r'^admin/', include('admin.urls')),
  url(r'^seller/', include('seller.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # url(r'^admin/', include(admin.site.urls)),
)
