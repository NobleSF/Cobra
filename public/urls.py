from django.conf.urls import patterns, include, url
from public.controller import home, account, checkout, product, artisan, collection

urlpatterns = patterns('',
  #home (site homepage) url defined in anou/urls.py
  url(r'^about$', home.about, name='about'),

  # product page at /product/123
  url(r'^product/(?P<id>\d+)$', product.home, name='product'),

  # artisan page at /artisan/123
  url(r'^artisan/(?P<id>\d+)$', artisan.home, name='artisan'),

  # collection at collection/newest or collection/artisan/123
  url(r'^collection/(?P<group>\w+)/?(?P<id>\d+)?$', collection.home, name='collection'),


  #Todo: I'd like to add the word "secure" into all account and checkout pages
    # just to give the user more peace of mind.

  #account pages
  url(r'^create$', account.create, name='create'),
  url(r'^login$', account.login, name='login'),
  url(r'^(?P<username>\w+)/logout$', account.logout, name='logout'),
  url(r'^(?P<username>\w+)/account$', account.home, name='account'),

  #checkout pages
  url(r'^(?P<username>\w+)/cart$', checkout.cart, name='cart'),
  url(r'^(?P<username>\w+)/payment$', checkout.payment, name='payment'),
  url(r'^(?P<username>\w+)/confirmation$', checkout.confirmation, name='confirmation'),

  #non-pages, ajax calls

)
