from django.conf.urls import patterns, include, url
from controller import account, product

urlpatterns = patterns('',

  url(r'^$', account.home, name='seller home'), #seller dashboard
  url(r'^edit$', account.edit, name='seller edit'), #edit seller info
  url(r'^asset$', account.asset, name='seller asset'), #create/update asset via ajax

  url(r'^product$', product.home, name='seller product'), #all products
  url(r'^product/create$', product.create, name='seller product create'),
  url(r'^product/(?P<id>\d+)$', product.detail, name='seller product detail'),
  url(r'^product/(?P<id>\d+)/edit$', product.edit, name='seller product edit'),
  url(r'^product/(?P<id>\d+)/delete$', product.delete, name='seller product delete'),

)
