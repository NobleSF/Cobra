from django.conf.urls import patterns, include, url
from apps.public.controller import home
from django.http import HttpResponseRedirect
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('',
  url(r'^$', home.home, name='home'), #fyi, this is home
  (r'^blog', redirect_to, {'url': 'http://helloanou.wordpress.com/'}),

  (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {}}),
  url(r'^humans.txt', direct_to_template, {'template':'humans.txt', 'mimetype':'text/plain'}),
  url(r'^robots.txt', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
)

urlpatterns += patterns('',
  url(r'^', include('apps.public.urls')),
  url(r'^', include('apps.admin.urls', namespace='admin')),
  url(r'^seller/', include('apps.seller.urls', namespace='seller')),
  url(r'^communication/', include('apps.communication.urls', namespace='communication')),
)

from django.views.generic.simple import direct_to_template
urlpatterns += patterns('',
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^humans\.txt$', direct_to_template,
     {'template': 'humans.txt', 'mimetype': 'text/plain'}),
)

#backwards compatability with old Anou site
from apps.communication.controller import sms
urlpatterns += patterns('',
  (r'^index.php', lambda x: HttpResponseRedirect('/')), #and this is home too
  (r'^landing.php', lambda x: HttpResponseRedirect('/')), #and this is home too
  (r'^a/', lambda x: HttpResponseRedirect('/seller/')), #and this is home too
)
