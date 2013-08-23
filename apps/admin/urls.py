from django.conf.urls import patterns, include, url
from controller import dashboard, account, products, communication, site_management

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#account pages
urlpatterns = patterns('',
  #Todo: I'd like to add the word "secure" into all account and checkout pages
    # just to give the user more peace of mind.

  url(r'^account/create$', account.create, name='account create'),
  url(r'^account/all_accounts$', account.all_accounts, name='all accounts'),
  url(r'^account/(?P<account_id>\d+)/edit$', account.edit, name='account edit'),
  url(r'^account/(?P<account_id>\d+)/password_reset$', account.reset_password, name='account reset password'),
  url(r'^account/login$', account.login, name='login'),
  url(r'^account/login_cheat$', account.login_cheat, name='login_cheat'),
  url(r'^account/logout$', account.logout, name='logout'),

)

#dashboard pages
urlpatterns += patterns('',
  url(r'^admin/dashboard$', dashboard.dashboard, name='dashboard'),

  #PRODUCTS
  url(r'^admin/review_products$', products.review_products, name='review products'),
  url(r'^admin/approve_product$', products.approve_product, name='approve product'),
  url(r'^admin/rate_product$', products.rate_product, name='rate product'),

  #ORDERS
  #url(r'^admin/place_order$', orders.place_order, name='place order'),

  #COMMUNICATION
  url(r'^admin/send_sms$', communication.sendSMS, name='send sms'),
  url(r'^admin/all_sms$', communication.allSMS, name='all sms'),
  url(r'^admin/all_email$', communication.allEmail, name='all email'),

  #SETTINGS
  url(r'^admin/management/country$', site_management.country, name='country'),
  url(r'^admin/management/currency$', site_management.currency, name='currency'),
  url(r'^admin/management/color$', site_management.color, name='color'),
  url(r'^admin/management/category$', site_management.category, name='category'),
  url(r'^admin/management/rating_subject$', site_management.rating_subject, name='rating_subject'),
  url(r'^admin/management/shipping_option$', site_management.shipping_option, name='shipping_option'),
  url(r'^admin/management/image_object$', site_management.image_object, name='image_object'),
)
