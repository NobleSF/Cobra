from django.conf.urls import patterns, include, url
from controller import sms, public_events, seller_events, order_events, testing

urlpatterns = patterns('',
  #email
  #url(r'^email/test$', public_events.test_email),

  #sms
  url(r'^sms/incoming$', sms.incoming, name='sms incoming'),
  url(r'^sms/status_confirmation$', sms.status_confirmation),

  #events
  url(r'^subscribe$', public_events.subscribe, name='subscribe'),
  url(r'^unsubscribe$', public_events.unsubscribe, name='unsubscribe'),

  #testing
  url(r'^order_emails$', testing.orders, name='order emails'),
)
