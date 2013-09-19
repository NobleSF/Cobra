from django.core.cache import cache

#async?
def invalidate_cache(fragment_name, *vary_on):
  try:
    cache_key = template_cache_key(fragment_name, *vary_on)
    cache.delete(cache_key)
  except:
    return False
  else:
    return True

def template_cache_key(fragment_name, *vary_on):
  # Builds a cache key for a template fragment
  from django.utils.hashcompat import md5_constructor
  from django.utils.http import urlquote

  base_cache_key = "template.cache.%s" % fragment_name
  args = md5_constructor(u":".join([urlquote(var) for var in vary_on]))
  return "%s.%s" % (base_cache_key, args.hexdigest())
