from django.conf.urls import patterns, include, url
from seller.controller import seller, product

urlpatterns = patterns('',

  url(r'^$', seller.home, name='seller home'), #seller dashboard
  url(r'^edit$', seller.edit, name='seller edit'), #edit seller info
  url(r'^asset$', seller.asset, name='seller asset'), #create/update asset via ajax

  url(r'^product$', product.home, name='seller product'), #all products
  url(r'^product/create$', product.create, name='seller product create'),
  url(r'^product/(?P<id>\d+)$', product.detail, name='seller product detail'),
  url(r'^product/(?P<id>\d+)/edit$', product.edit, name='seller product edit'),
  url(r'^product/(?P<id>\d+)/delete$', product.delete, name='seller product delete'),

)
