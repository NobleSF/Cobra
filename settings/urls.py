from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.sitemaps import views as sitemap_views

from sitemaps import sitemaps
from apps.admin.views import account
from apps.public.views import home

urlpatterns = [
  url(r'^$', home.home, name='home'), #fyi, this is home


  #APPS
  url(r'^', include('apps.public.urls')),
  url(r'^admin/', include('apps.admin.urls', namespace='admin')),
  url(r'^seller/', include('apps.seller.urls', namespace='seller')),
  url(r'^commission/', include('apps.commission.urls', namespace='commission')),
  url(r'^communication/', include('apps.communication.urls', namespace='communication')),


  #TOP LEVEL URLS
  url(r'^blog', RedirectView.as_view(url='http://helloanou.wordpress.com/', permanent=False), name='blog'),
  url(r'^login', account.login, name='login'),
  url(r'^logout', account.logout, name='logout'),


  #for Flickr photo check run by IFTTT every hour to wake up Heroku
  url(r'^logo',
      RedirectView.as_view(url='http://s3.amazonaws.com/anou/images/Anou_logo_80x50.png',
                           permanent=False)),


  #SEO
  url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
  url(r'^humans\.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),


  #SITEMAP
  url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


  #SITE-VERIFICATIONS
  url(r'^pinterest-73682\.html',
      TemplateView.as_view(template_name='site-verifcations/pinterest-73682.html')),
  url(r'^google79499a3cc417dc54.html',
      TemplateView.as_view(template_name='site-verifcations/google79499a3cc417dc54.html')),
  url(r'^loaderio-26fc148a154773260da4400ae4adb1a6.txt',
      TemplateView.as_view(template_name='site-verifcations/loaderio-26fc148a154773260da4400ae4adb1a6.txt')),
]
