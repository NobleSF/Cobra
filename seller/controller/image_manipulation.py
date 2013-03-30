def makeThumbnails(image_url):
  from PIL import Image as pil
  from cStringIO import StringIO
  from urllib2 import urlopen
  from anou.settings import DEBUG, THUMBNAIL_ALIASES

  original_dimensions = THUMBNAIL_ALIASES['original']['size']
  thumb_dimensions    = THUMBNAIL_ALIASES['thumb']['size']
  pinky_dimensions    = THUMBNAIL_ALIASES['pinky']['size']

  original_image = pil.open(StringIO(urlopen(image_url).read()))

  new_original  = scaleImage(original_image, original_dimensions)
  thumb         = scaleImage(original_image, thumb_dimensions)
  pinky         = scaleImage(original_image, pinky_dimensions)

  return (new_original, thumb, pinky)

def scaleImage(img, dimensions, force=True):
  """ Scale the given image, optionally cropping it
      to make sure the result image has
      the specified width and height.
  """
  from PIL import Image as pil
  from cStringIO import StringIO

  (max_width, max_height) = dimensions

  if not force:
    img.thumbnail((max_width, max_height), pil.ANTIALIAS)
  else:
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = max_width, max_height
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
      crop_height = src_height
      crop_width = crop_height * dst_ratio
      x_offset = float(src_width - crop_width) / 2
      y_offset = 0
    else:
      crop_width = src_width
      crop_height = crop_width / dst_ratio
      x_offset = 0
      y_offset = float(src_height - crop_height) / 3

    img = img.crop((int(x_offset), int(y_offset), int(x_offset)+int(crop_width), int(y_offset)+int(crop_height)))
    img = img.resize((int(dst_width), int(dst_height)), pil.ANTIALIAS)

  img.seek(0)
  output_image = StringIO()
  img.save(output_image, 'JPEG')
  return output_image.getvalue()
