from apps.etsy import models, api
from django.utils import timezone

class Transaction(object):

  def __init__(self, transaction_id, shop=None):
    self.transaction_id = transaction_id

    try:
      self.transaction = models.Transaction.objects.get(trasaction_id=trasaction_id)

    except models.Transaction.DoesNotExist:
      self.transaction = self.createTransaction()

  def createTransaction(self, trasaction_id):
    transaction_data = getTransaction(trasaction_id)

    shop = models.Shop.objects.get(user_id = seller_user_id)
    listing = models.Listing.objects.get(listing_id=listing_id)

    models.Transaction(trasaction_id  = trasaction_id,
                       shop           = shop,
                       listing        = listing,
                       receipt_id     = receipt_id,
                       )

  def getTransaction(self):
    """
    https://www.etsy.com/developers/documentation/reference/transaction#method_gettransaction
    """
    etsy = api.Etsy()
    method = 'GET'
    uri = 'transactions/%d' % self.transaction_id

    return transaction_data

  def updateReceipt(self):
    """
    https://www.etsy.com/developers/documentation/reference/receipt#method_updatereceipt
    """
    etsy = api.Etsy()
    method = 'POST'
    uri = 'receipts/%d' % self.transaction.receipt_id


  def submitTracking(self):
    """
    https://www.etsy.com/developers/documentation/reference/receipt#method_submittracking
    """
    etsy = api.Etsy(OAuth=True)
    method = 'POST'
    uri = ('/shops/%d/receipts/%d/tracking' %
           (self.transaction.shop.shod_id, self.transaction.receipt_id ))

    parameters = {
      'tracking_code':      self.transaction.order.tracking_number,
      'carrier_name':       self.transaction.order.shipping_carrier,
      'send_bcc':           True,
    }
