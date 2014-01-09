from django import template
register = template.Library()

@register.simple_tag
def sizescaler(value, max_value, max_scale_size, min_scale_size=0, adder=0):
  normalized = float(value) / max_value
  scaled = normalized * (max_scale_size - min_scale_size)
  fitted = scaled if scaled > min_scale_size else min_scale_size
  return int(fitted + adder)

@register.simple_tag
def inversesizescaler(value, max_value, max_scale_size, min_scale_size=0, adder=0):
  normalized = float(max_value - value) / max_value
  scaled = normalized * (max_scale_size - min_scale_size)
  fitted = scaled if scaled > min_scale_size else min_scale_size
  return int(fitted + adder)
