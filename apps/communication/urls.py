from django.conf.urls import patterns, include, url
from controller import events, sms

urlpatterns = patterns('',
  #email
  url(r'^email/test$', events.test_email),

  #sms
  url(r'^sms/incoming$', sms.incoming, name='sms incoming'),
  url(r'^sms/status_confirmation$', sms.status_confirmation),
)
