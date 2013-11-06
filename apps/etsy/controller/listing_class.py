from apps.etsy import models, api
from django.utils import timezone

class Listing(object):

  def __init__(self, seller, etsy_shop_name=""):
    try:
      self.listing = models.Listing.objects.get(seller=seller)

    except models.Shop.DoesNotExist:
      self.shop = self.createFromSeller(seller, etsy_shop_name)

  def createListing(self):
    """
    https://www.etsy.com/developers/documentation/reference/listing#method_createlisting
    """
    etsy = api.Etsy()
    method  = "POST"
    uri     = "listings"

    parameters = {
      'quantity':             self.listing.quantity,
      'title':                self.listing.title,
      'description':          self.listing.description,
      'price':                self.listing.price,
      'materials':            self.listing.materials,
      #'shipping_template_id': '123'
      #'shop_section_id'
      #'image_ids'
      'is_customizable':      self.listing.is_customizable,
      #image

      #'state':               defaults to 'active',
      'processing_min':       self.listing.processing_min,
      'processing_max':       self.listing.processing_max,
      #'category_id'
      'tags':                 self.listing.tags,
      'who_made':             self.listing.who_made,
      'is_supply':            self.listing.is_supply,
      'when_made':            self.listing.when_made,
      'recipient':            self.listing.recipient,
      #'occasion'
      'style':                self.listing.style,
    }


    etsy_listing = response_data
    self.listing.listing_id = etsy_listing['listing_id']
    self.listing.listed_at = timezone.now()
    self.listing.listed_price = etsy_listing['price']
    self.listing.save()

  def getListing(self):
    """
    https://www.etsy.com/developers/documentation/reference/listing#method_getlisting
    """
    etsy = api.Etsy()
    method  = "GET"
    uri     = "listings/%d" % self.listing_id
    #no parameters

    #etsy_listing = response_data

  def updateListing(self, renew=False):
    """
    https://www.etsy.com/developers/documentation/reference/listing#method_updatelisting
    """
    etsy = api.Etsy()
    method  = "PUT"
    uri     = "listings/%d" % self.listing_id
    #if self.listing.sold_at: don't update

    parameters = {
      'listing_id':           self.listing.listing_id,
      'renew':                renew,
      'state':                'inacitve' if not renew else 'active',

      'quantity':             self.listing.quantity,
      'title':                self.listing.title,
      'description':          self.listing.description,
      'price':                self.listing.price,
      'materials':            self.listing.materials,
      'is_customizable':      self.listing.is_customizable,

      #category_id
      'tags':                 self.listing.tags,
      #'who_made':
      #'is_supply':
      #'when_made':
      #'recipient':

      #'occasion':
      'style':                self.listing.style,

      'processing_min':       self.listing.processing_min,
      'processing_max':       self.listing.processing_max,
      #'featured_rank':        self.listing.product.rank_position_by_seller
    }

    for photo in self.product.photos:
      if photo.updated_at > self.synced_at:
        self.uploadListingImage(photo.rank)

    if etsy_listing['status'] == 'active':
      self.listing.unlisted_at = None
      self.listing.sold_at = None

    self.synced_at = timezone.now()
    self.save()

  def deleteListing(self):
    """
    https://www.etsy.com/developers/documentation/reference/listing#method_deletelisting
    """
    etsy = api.Etsy()
    method  = "DELETE"
    uri     = "listings/%d" % self.listing_id
    #no parameters

    #etsy_listing = response_data


  def uploadListingImage(self, rank):
    """
    https://www.etsy.com/developers/documentation/reference/listingimage
    http://blog.liangzan.net/blog/2012/08/27/uploading-images-via-etsy-api-with-ruby/
    """
    etsy = api.Etsy()
    method = 'POST'
    uri = '/listings/%d/images' % self.listing_id

    image_location = self.product.photos.get(rank=rank).original

    parameters = {
      #'listing_image_id':
      'image':                  image_location,
      'rank':                   rank,
      'overwrite':              True,
    }

  def createShippingTemplate(self):
    """
    https://www.etsy.com/developers/documentation/reference/shippingtemplate#method_createshippingtemplate
    """
    etsy = api.Etsy()
    method  = "GET"
    uri     = "shipping/templates/%d" % self.shipping_template_id

    parameters = {
                  'title':                  'USA',
                  'origin_country_id':      147, #morocco
                  'destination_country_id': 209, #USA
                  'primary_cost':           0.00,
                  'secondary_cost':         0.00,
                  }
