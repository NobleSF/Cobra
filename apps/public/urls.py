from django.conf.urls import patterns, include, url
from controller import home, checkout, product, store, custom_order

urlpatterns = patterns('',

  #homepage url defined in anou/urls.py
  url(r'^load_products$', home.loadProducts, name='load products'),
  url(r'^about$', home.about, name='about'),

  # PRODUCT PAGE at /product/123-slug
  url(r'^product/(?P<product_id>\d+)-(?P<slug>\S+)$', product.home,
      name='product_w_slug'),
  url(r'^product/(?P<product_id>\d+)$', product.home, name='product'),

  # COMMANDS / CUSTOM ORDERS
  url(r'^product/custom_order_estimate$', custom_order.estimate,
      name='custom order estimate'),
  url(r'^product/custom_order_request$', custom_order.request,
      name='custom order request'),

  # STORE PAGE at /store/123 represents a seller profile
  url(r'^store/(?P<seller_id>\d+)-(?P<slug>\S+)', store.home,
      name='store_w_slug'),
  url(r'^store/(?P<seller_id>\d+)$', store.home, name='store'),

  # CHECKOUT PAGES
  url(r'^checkout/cart$', checkout.cart, name='cart'),
  url(r'^checkout/cart-add/(?P<product_id>\d+)$', checkout.cartAdd,
      name='cart-add'),
  url(r'^checkout/cart-remove/(?P<product_id>\d+)$', checkout.cartRemove,
      name='cart-remove'),
  url(r'^checkout/ajax/cart_save$', checkout.cartSave, name='cart-save'),
  url(r'^checkout/ajax/admin_checkout$', checkout.adminCheckout,
      name='admin checkout'),
  url(r'^checkout/confirmation$', checkout.confirmation, name='confirmation'),

  #temporary
  url(r'^commonthread$', home.commonthread, name='commonthread'),
  url(r'^commonthread/buy/(?P<rug_name>\S+)$', home.commonthreadAddToCart,
      name='buy commonthread rug'),

  #testing
  url(r'^product_data', product.product_data, name='product_data'),
  url(r'^test_meta$', home.test_meta, name='test meta'),
)
