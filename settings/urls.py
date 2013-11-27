from django.conf.urls import patterns, include, url
from apps.public.controller import home
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.generic.simple import redirect_to, direct_to_template
from .sitemaps import sitemaps

urlpatterns = patterns('',
  url(r'^$', home.home, name='home'), #fyi, this is home
  url(r'^blog', redirect_to,
      {'url': 'http://helloanou.wordpress.com/', 'permanent': False}, name='blog'),
)

urlpatterns += patterns('',
  url(r'^', include('apps.public.urls')),
  url(r'^', include('apps.admin.urls', namespace='admin')),
  url(r'^seller/', include('apps.seller.urls', namespace='seller')),
  url(r'^communication/', include('apps.communication.urls', namespace='communication')),
)

#BACKWARDS COMPATABILITY WITH OLD ANOU SITE
from apps.communication.controller import sms
urlpatterns += patterns('',
  (r'^index.php', lambda x: HttpResponsePermanentRedirect('/')),
  (r'^landing.php', lambda x: HttpResponsePermanentRedirect('/')),
  (r'^a/', lambda x: HttpResponsePermanentRedirect('/seller/')),

  #for Flickr photo check run by IFTTT every hour to wake up Heroku
  (r'^logo$', redirect_to,
   {'url': 'http://s3.amazonaws.com/anou/images/Anou_logo_80x50.png', 'permanent': False}),
)

#SEO
urlpatterns += patterns('',
  (r'^robots\.txt', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
  (r'^humans\.txt', direct_to_template, {'template':'humans.txt', 'mimetype':'text/plain'}),
)
urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

#SITE-VERIFICATIONS
urlpatterns += patterns('',
  (r'^pinterest-73682.html', direct_to_template,
    {'template': 'site-verifcations/pinterest-73682.html'}),
  (r'^google79499a3cc417dc54.html', direct_to_template,
    {'template': 'site-verifcations/google79499a3cc417dc54.html'}),
  (r'^loaderio-26fc148a154773260da4400ae4adb1a6.txt', direct_to_template,
    {'template': 'site-verifcations/loaderio-26fc148a154773260da4400ae4adb1a6.txt'}),
)
