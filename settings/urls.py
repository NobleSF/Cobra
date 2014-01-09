from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.generic import TemplateView, RedirectView

from apps.public.controller import home
urlpatterns = patterns('',
  url(r'^$', home.home, name='home'), #fyi, this is home
)

#APPS
urlpatterns += patterns('',
  url(r'^', include('apps.public.urls')),
  url(r'^admin/', include('apps.admin.urls', namespace='admin')),
  url(r'^seller/', include('apps.seller.urls', namespace='seller')),
  url(r'^communication/', include('apps.communication.urls', namespace='communication')),
)

#TOP LEVEL URLS
from apps.admin.controller import account
urlpatterns += patterns('',
  url(r'^blog',
      RedirectView.as_view(url='http://helloanou.wordpress.com/', permanent=False), name='blog'),
  url(r'^login$', account.login, name='login'),
  url(r'^logout$', account.logout, name='logout'),
)

#OLD SITE REDIRECTS
from apps.communication.controller import sms
urlpatterns += patterns('',
  (r'^index.php', lambda x: HttpResponsePermanentRedirect('/')),
  (r'^landing.php', lambda x: HttpResponsePermanentRedirect('/')),
  (r'^a/', lambda x: HttpResponsePermanentRedirect('/seller/')),

  #for Flickr photo check run by IFTTT every hour to wake up Heroku
  url(r'^logo',
      RedirectView.as_view(url='http://s3.amazonaws.com/anou/images/Anou_logo_80x50.png',
                           permanent=False))
)

#SEO
urlpatterns += patterns('',
  url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
  url(r'^humans\.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
)
from .sitemaps import sitemaps
urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

#SITE-VERIFICATIONS
urlpatterns += patterns('',
  url(r'^pinterest-73682\.html',
      TemplateView.as_view(template_name='site-verifcations/pinterest-73682.html')),
  url(r'^google79499a3cc417dc54.html',
      TemplateView.as_view(template_name='site-verifcations/google79499a3cc417dc54.html')),
  url(r'^loaderio-26fc148a154773260da4400ae4adb1a6.txt',
      TemplateView.as_view(template_name='site-verifcations/loaderio-26fc148a154773260da4400ae4adb1a6.txt')),
)
