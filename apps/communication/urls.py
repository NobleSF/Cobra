from django.conf.urls import patterns, include, url
from controller import events, sms

urlpatterns = patterns('',
  url(r'^incoming$', sms.incoming, name='sms incoming'),


)
