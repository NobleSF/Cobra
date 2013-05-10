from django.conf.urls import patterns, include, url
from django.contrib import admin
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls),
)
