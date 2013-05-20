from apps.seller import models
class Product:
  def __init__(self, request):
    try:
      self.product = models.Product.objects.get(id=request.product_id)
    except:
      self.product = self.new(request)

  def __iter__(self):
    for asset in self.product.asset_set.all():
      yield asset

  def new(self, request):
    product = models.Product()
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

  def addAsset(self, asset_id):
    asset = models.Asset.objects.get(id=asset_id)
    if asset:
      self.product.assets.add(asset)
    else:
      raise ModelError('asset-id does not exist')

  def removeAsset(self, asset_id):
    asset = models.Asset.objects.get(id=asset_id)
    if asset:
      self.product.assets.remove(asset)
    else:
      pass #i don't care

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
      raise Exception
    else:
      return value

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
      raise Exception
    else:
      return value


  def clear(self):
    try:
      self.product.assets.clear()
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
      self.product.delete()
