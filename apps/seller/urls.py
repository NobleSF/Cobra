from django.conf.urls import patterns, include, url
from controller import seller, account, inventory, cloudinary_upload, custom_order, edit_product

urlpatterns = patterns('',
  url(r'^$', seller.home, name='home'), #seller dashboard, live products

  #SELLER ACCOUNT
  url(r'^edit$', account.edit, name='edit'), #edit seller info
  url(r'^ajax/asset_save$', account.saveAsset, name='save asset'),
  url(r'^ajax/asset_delete$', account.deleteAsset, name='delete asset'),

  #INVENTORY
  url(r'^products$', inventory.products, name='products'), #products
  url(r'^orders$', inventory.orders, name='orders'), #orders

  url(r'^inventory/create$', inventory.create, name='inventory create'),
  url(r'^inventory/(?P<product_id>\d+)/remove$', inventory.remove, name='inventory remove'),

  url(r'^inventory/(?P<product_id>\d+)/edit$', edit_product.edit, name='edit product'),

  #PHOTOS AND IMAGES
  url(r'^ajax/pho_data$', cloudinary_upload.photoFormData, name='photo form data'),
  url(r'^ajax/img_data$', cloudinary_upload.imageFormData, name='image form data'),

  url(r'^ajax/chk_pho_up$', cloudinary_upload.checkPhotoUpload, name='check photo upload'),
  url(r'^ajax/chk_img_up$', cloudinary_upload.checkImageUpload, name='check image upload'),

  url(r'^ajax/complete_up$', cloudinary_upload.completeUpload, name='complete upload'),

  # CUSTOM ORDERS
)
