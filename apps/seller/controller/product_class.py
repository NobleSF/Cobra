from apps.seller import models
from apps.admin import models as admin_models
from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.communication.controller.email_class import Email
from settings import people

class Product(object):
  def __init__(self, product_id=None, request=None):
    try:
      if product_id:
        self.product = (models.Product.objects.get(id=product_id))

        if request:
          #admin_type = request.session.get('admin_type')
          #admin_type not in ['master', 'country', 'trainer']

          #don't let sellers edit each others products, but admins can edit anyone's
          if (not 'admin_id' in request.session and
              int(request.session['seller_id']) != self.product.seller.id):
            self.product = None
            raise Exception("Not Authorized")

      elif request and 'seller_id' in request.session:
        self.new(request.session['seller_id'])

      else:
        raise Exception("No product_id or valid request object")

    except Exception as e:
      self.product = None
      #possibly bad product id or no seller_id in request.session
      ExceptionHandler(e, "problem in product_class.Product.__init__")

  def __iter__(self):
    for asset in self.product.asset_set.all():
      yield asset

  def new(self, seller_id):
    self.product = models.Product(seller_id=seller_id)
    self.product.save()

  def belongsToPhone(self, phone_number):
    try:
      seller_phone = self.product.seller.account.phone
      return True if (phone_number[-8:] == seller_phone[-8:]) else False
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.belongsToPhone")
      return False

  def addPhoto(self, url, rank):
    from apps.seller.models import Photo
    try:
      photo, is_new = Photo.objects.get_or_create(
                        product = self.product,
                        rank = rank
                      )
      photo.original = url
      photo.save()
    except Exception as e:
      return str(e)
    else:
      return photo

  def photos(self):
    return self.product.photos.all().order_by('rank')

  def addAsset(self, asset_id):
    try:
      asset = models.Asset.objects.get(id=asset_id)
      self.product.assets.add(asset)
      return "added asset " + (asset.name if asset.name else "")

    except models.Asset.DoesNotExist:
      return "asset does not exist"
    except Exception as e: return str(e)

  def removeAsset(self, asset_id):
    try:
      asset = models.Asset.objects.get(id=asset_id)
      self.product.assets.remove(asset)
    except: pass
    finally:
      return "removed asset"

  def addShippingOption(self, shipping_option_id):
    try:
      shipping_option = models.ShippingOption.objects.get(id=shipping_option_id)
      self.product.shipping_options.add(shipping_option)
      return "added shipping option " + (shipping_option.name if shipping_option.name else "")

    except models.ShippingOption.DoesNotExist:
      return "shipping option does not exist"
    except Exception as e: return str(e)

  def removeShippingOption(self, shipping_option_id):
    try:
      shipping_option = models.ShippingOption.objects.get(id=shipping_option_id)
      self.product.shipping_options.remove(shipping_option)
    except: pass
    finally:
      return "shipping option removed"

  def addColor(self, color_id):
    try:
      color = admin_models.Color.objects.get(id=color_id)
      self.product.colors.add(color)
      return "added color " + color.name
    except admin_models.Color.DoesNotExist:
      return "color does not exist"
    except: return ""

  def removeColor(self, color_id):
    try:
      color = admin_models.Color.objects.get(id=color_id)
      self.product.colors.remove(color)
    except: pass
    finally: return "color removed"

  def update(self, attribute, value):
    try:
      value = int(round(float(value))) if value else None
    except:
      value = None
    try:
      if attribute == 'price':
        self.product.price = value
      elif attribute == 'length':
        self.product.length = value
      elif attribute == 'width':
        self.product.width = value
      elif attribute == 'height':
        self.product.height = value
      elif attribute == 'weight':
        self.product.weight = value
      else:
        raise Exception('attribute does not exist')

    except Exception as e:
      return str(e)
    else:
      self.product.save()
      return "saved " + attribute + ": " + (str(value) if value else "None")

  def get(self, attribute):
    try:
      if attribute == 'price':
        value = self.product.price
      elif attribute == 'length':
        value = self.product.length
      elif attribute == 'width':
        value = self.product.width
      elif attribute == 'height':
        value = self.product.height
      elif attribute == 'weight':
        value = self.product.weight
      else:
        raise Exception('attribute does not exist')

    except Exception as e:
      return str(e)
    else:
      return str(value) if value else ""

  def clear(self):
    try:
      self.product.assets.clear()
      self.product.shipping_options.clear()
      self.product.colors.clear()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.clear")

  def activate(self):
    try:
      #todo: if self.product.is_complete
      self.product.active_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.activate")
    else:
      Email('product/activated', self.product).sendTo(people.Dan.email)

  def deactivate(self):
    from apps.communication.controller.order_events import cancelOrder
    try:
      for order in self.product.order_set.all():
        cancelOrder(order)
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.deactivateA")

    try:
      self.product.deactive_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.deactivateB")
    else:
      try:
        message = "R %d" % self.product.id
        message += "<br>%s" % self.product.seller.name
        Email(message=message).sendTo(people.everyones_emails)
      except Exception as e:
        ExceptionHandler(e, "in product_class.Product.deactivateC")

  def approve(self):
    try:
      self.product.approved_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
      self.product.resetSlug()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.approve")

  def unapprove(self): #remove original approval
    try:
      self.product.approved_at = None
      self.product.in_holding = False
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.unapprove")

  def disapprove(self): #set to not approved
    try:
      self.product.approved_at = None
      self.product.in_holding = False
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.disapprove")

  def hold(self):
    try:
      self.product.approved_at = None
      self.product.in_holding = True
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.hold")

  def sold(self):
    try:
      self.product.sold_at = timezone.now()
      self.product.save()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.sold")

  def delete(self):
    try: self.product.assets.clear()
    except: pass

    try:
      self.product.delete()
    except Exception as e:
      ExceptionHandler(e, "in product_class.Product.delete")
