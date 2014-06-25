import random

GOLDEN_RATIO = 0.618033988749895

def get_pastel(seed=None):
  if seed:
    random.seed(seed)
  hue = random.random()
  hue = hue + GOLDEN_RATIO
  hue = hue % 1
  return hsv_to_rgb(hue, 0.5, 0.95)

# HSV values in [0..1[
# returns [r,g,b] values from 0 to 255
def hsv_to_rgb(hue, saturation, value):
  hue_int = int(hue*6)
  f = hue * 6 - hue_int
  p = value * (1 - saturation)
  q = value * (1 - f*saturation)
  t = value * (1 - (1 - f) * saturation)
  v = value

  if hue_int == 0:
    r,g,b = v,t,p
  if hue_int == 1:
    r,g,b = q,v,p
  if hue_int == 2:
    r,g,b = p,v,t
  if hue_int == 3:
    r,g,b = p,q,v
  if hue_int == 4:
    r,g,b = t,p,v
  if hue_int == 5:
    r,g,b = v,p,q

  r,g,b = (r*256), (g*256), (b*256)

  return "rgb(%d,%d,%d)" % (int(round(r)), int(round(g)), int(round(b)))
