from django.conf.urls import patterns, include, url
from controller import home, checkout, product, store

urlpatterns = patterns('',
  #home (site homepage) url defined in anou/urls.py
  url(r'^about$', home.about, name='about'),
  url(r'^contact$', home.contact, name='contact'),

  # product page at /product/123
  url(r'^product/(?P<product_id>\d+)$', product.home, name='product'),

  # search at search/newest or search/carpets/red/length_50-100
  # we need a big regex to pull the keywords from the url here instead of putting that logic in the controller
  url(
    r'^search[((/type_(?P<category>\w+))?|(/color_(?P<color>\w+))?|/(?P<collection>\w+))?]+$',
    home.search, name='search'),
  #url(r'^search(/(?P<keywords>\w+))+$', home.search, name='search'),

  # store page at /store/123 represents a seller profile
  url(r'^store/(?P<seller_id>\d+)$', store.home, name='store'),


  #checkout pages
  url(r'^checkout/cart$', checkout.cart, name='cart'),
  url(r'^checkout/cart-add/(?P<product_id>\d+)$', checkout.cartAdd, name='cart-add'),
  url(r'^checkout/cart-remove/(?P<product_id>\d+)$', checkout.cartRemove, name='cart-remove'),
  url(r'^checkout/confirmation$', checkout.confirmation, name='confirmation'),

  #non-pages, ajax calls
  url(r'^test_meta$', home.test_meta, name='test meta'),
)
