from apps.seller import models
from apps.admin import models as admin_models
class Product:
  def __init__(self, request):
    try:
      self.product = models.Product.objects.filter(seller_id=request.session['seller_id']).get(id=request.product_id)
    except:
      self.product = self.new(request)

  def __iter__(self):
    for asset in self.product.asset_set.all():
      yield asset

  def new(self, request):
    product = models.Product(seller_id = request.session['seller_id'])
    product.save()
    request.product_id = product.id
    return product

  def addPhoto(self, url, rank, photo_id=None):
    if photo_id:
      photo = models.Photo.objects.get(id=photo_id)
    else:
      photo = models.Photo(product=self.product, rank=rank, original=url)

    photo.thumb = url.replace("upload", "upload/t_thumb")
    photo.pinky = url.replace("upload", "upload/t_pinky")
    photo.save()
    return photo

  def photos(self):
    return self.product.photo_set.all().order_by('rank')

  def addAsset(self, asset_id):
    asset = models.Asset.objects.get(id=asset_id)
    if asset:
      self.product.assets.add(asset)
      return "added asset " + asset.name
    else:
      return "asset does not exist"

  def removeAsset(self, asset_id):
    asset = models.Asset.objects.get(id=asset_id)
    if asset:
      self.product.assets.remove(asset)

  def addShippingOption(self, shipping_option_id):
    shipping_option = models.ShippingOption.objects.get(id=shipping_option_id)
    if shipping_option:
      self.product.shipping_options.add(shipping_option)
      return "added shipping option " + shipping_option.name
    else:
      return "shipping option does not exist"

  def removeShippingOption(self, shipping_option_id):
    shipping_option = models.ShippingOption.objects.get(id=shipping_option_id)
    if shipping_option:
      self.product.shipping_options.remove(shipping_option)

  def addColor(self, color_id):
    color = admin_models.Color.objects.get(id=color_id)
    if color:
      self.product.colors.add(color)
      return "added color " + color.name
    else:
      return "color does not exist"

  def removeColor(self, color_id):
    color = admin_models.Color.objects.get(id=color_id)
    if color:
      self.product.colors.remove(color)

  def update(self, attribute, value):
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
      return "saved " + attribute + ": " + value

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
      raise e
    else:
      return value


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
      self.product.is_active = True
      self.product.save()
    except:
      return False
    else:
      return True

  def deactivate(self):
    try:
      self.product.is_active = False
      self.product.save()
    except:
      return False
    else:
      return True

  def remove(self): #old, marked for deletion
    try:
      self.product.is_active = False
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
