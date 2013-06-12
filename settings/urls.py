from django.conf.urls import patterns, include, url
from apps.public.controller import home
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
  url(r'^$', home.home, name='home'), #fyi, this is home
  (r'^index.php$', lambda x: HttpResponseRedirect('/')), #and this is home too

  #url(r'^humans.txt', return_static_file('humans.txt')),
  #url(r'^robots.txt', return_static_file('robots.txt')),
)

urlpatterns += patterns('',
  url(r'^', include('apps.public.urls')),
  url(r'^', include('apps.admin.urls', namespace='admin')),
  url(r'^seller/', include('apps.seller.urls', namespace='seller')),
)

from django.views.generic.simple import direct_to_template
urlpatterns += patterns('',
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^humans\.txt$', direct_to_template,
     {'template': 'humans.txt', 'mimetype': 'text/plain'}),
)
