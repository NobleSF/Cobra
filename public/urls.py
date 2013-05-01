from django.conf.urls import patterns, include, url
from controller import home, checkout, product, store

urlpatterns = patterns('',
  #home (site homepage) url defined in anou/urls.py
  url(r'^about$', home.about, name='about'),
  url(r'^contact$', home.contact, name='contact'),

  # product page at /product/123
  url(r'^product/(?P<product_id>\d+)$', product.home, name='product'),

  # collection at collection/newest or collection/store/woodshop-brahim
  url(r'^collection/(?P<group>\w+)/?(?P<name>\w+)?$', product.collection, name='collection'),

  # store page at /store/123 represents a seller profile
  url(r'^store/(?P<seller_id>\d+)$', store.home, name='store'),


  #checkout pages
  url(r'^checkout/cart$', checkout.cart, name='cart'),
  url(r'^checkout/payment$', checkout.payment, name='payment'),
  url(r'^checkout/confirmation$', checkout.confirmation, name='confirmation'),

  #non-pages, ajax calls
  url(r'^test_meta$', home.test_meta, name='test meta'),
)
