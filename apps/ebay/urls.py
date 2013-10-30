from django.conf.urls import patterns, include, url
from controller import main

urlpatterns = patterns('',
  #testing
  url(r'^test$', main.test, name='test'),
)
