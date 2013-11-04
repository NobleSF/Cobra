from django.conf.urls import patterns, include, url
from controller import home, checkout, product, store

urlpatterns = patterns('',
  #home (site homepage) url defined in anou/urls.py
  url(r'^about$', home.about, name='about'),

  # product page at /product/123
  url(r'^product/(?P<product_id>\d+)', product.home, name='product'),
  url(r'^product/(?P<product_id>\d+)-(?P<slug>\w+)', product.home, name='product_w_slug'),


  # store page at /store/123 represents a seller profile
  url(r'^store/(?P<seller_id>\d+)$', store.home, name='store'),

  #checkout pages
  url(r'^checkout/cart$', checkout.cart, name='cart'),
  url(r'^checkout/cart-add/(?P<product_id>\d+)$', checkout.cartAdd, name='cart-add'),
  url(r'^checkout/cart-remove/(?P<product_id>\d+)$', checkout.cartRemove, name='cart-remove'),
  url(r'^checkout/ajax/cart_save$', checkout.cartSave, name='cart-save'),
  url(r'^checkout/ajax/admin_checkout$', checkout.adminCheckout, name='admin checkout'),
  url(r'^checkout/confirmation$', checkout.confirmation, name='confirmation'),

  #testing
  url(r'^test_meta$', home.test_meta, name='test meta'),
)
