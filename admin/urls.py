from django.conf.urls import patterns, include, url
from controller import account

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

  #Todo: I'd like to add the word "secure" into all account and checkout pages
    # just to give the user more peace of mind.

  #account pages
  url(r'^create$', account.create, name='create'),
  url(r'^login$', account.login, name='login'),
  url(r'^logout$', account.logout, name='logout'),
  url(r'^(?P<username>\w+)$', account.home, name='account'),

)
