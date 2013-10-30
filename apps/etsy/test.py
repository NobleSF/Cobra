from apps.etsy.controller.shop_class import Shop
from apps.etsy.controller.listing_class import Listing

from apps.seller.models import Seller, Product

test_store_id = 38935068
test_shop_id  = 7949852

def go():
  seller = Seller.objects.get(account__username='seller')
  shop = Shop(seller, "CoopKhenifra")
  #shop.updateShop()
  return shop
