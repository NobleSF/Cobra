from apps.seller import models
from apps.admin import models as admin_models
from django.utils import timezone
from apps.communication.controller import seller_events
from apps.admin.utils.exception_handling import ExceptionHandler

class Product(object):
  def __init__(self, request=None, product=None):
    try:
      if request:
        self.product = (models.Product.objects.get(id=request.product_id))

        #don't let sellers edit each others products, but admins can edit anyone's
        if (not 'admin_id' in request.session and
            int(request.session['seller_id']) != self.product.seller.id):
          self.product = None

      else:
        self.product = product

    except Exception as e:
      if request:
        self.product = self.new(request)
      else:
        ExceptionHandler(e, "problem in product_class.Product.__init__")

  def __iter__(self):
    for asset in self.product.asset_set.all():
      yield asset

  def new(self, request):
    product = models.Product(seller_id = request.session['seller_id'])
    product.save()
    request.product_id = product.id
    return product

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
    except Asset.DoesNotExist:
      return "asset does not exist"
    except: return ""

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
    except ShippingOption.DoesNotExist:
      return "shipping option does not exist"
    except: return ""

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
    except ShippingOption.DoesNotExist:
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
        raise TypeError('attribute does not exist')

    except Exception as e:
      return "attribute does not exist"
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
        raise TypeError('attribute does not exist')

    except Exception as e:
      return "attribute does not exist"
    else:
      return str(value) if value else ""

  def clear(self):
    try:
      self.product.assets.clear()
      self.product.shipping_options.clear()
      self.product.colors.clear()
    except:
      return False
    else:
      return True

  def activate(self):
    try:
      #todo: if self.product.is_complete
      self.product.active_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
    except:
      return False
    else:
      seller_events.activatedProduct(self.product)
      return True

  def deactivate(self):
    try:
      self.product.deactive_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
    except:
      return False
    else:
      return True

  def approve(self):
    try:
      self.product.approved_at = timezone.now()
      self.product.in_holding = False
      self.product.save()
    except:
      return False
    else:
      return True

  def unapprove(self):
    try:
      self.product.approved_at = None
      self.product.in_holding = False
      self.product.save()
    except:
      return False
    else:
      return True

  def disapprove(self):
    try:
      self.product.approved_at = None
      self.product.in_holding = False
      self.product.save()
    except:
      return False
    else:
      return True

  def mark_sold(self):
    try:
      self.product.sold_at = timezone.now()
      self.product.save()
    except:
      return False
    else:
      return True

  def delete(self):
    try:
      self.product.assets.clear()
    except:
      pass
    finally:
      try:
        self.product.delete()
      except:
        return False
      else:
        return True
