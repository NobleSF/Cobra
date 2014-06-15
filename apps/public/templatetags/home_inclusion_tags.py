from django import template
register = template.Library()

@register.inclusion_tag('home/homepage_listings.html')
def homepage_listings_tag():
  from apps.api.models.listing import Listing
  from apps.public.controllers.listing_ranking import updateRankings

  listings = Listing.objects.for_sale().exclude(ranking=None)
  #sort by average ranking points, descending
  listings = sorted(listings, key=lambda p: p.ranking.weighted_average)
  listings.reverse()
  return {'listings':listings}

@register.inclusion_tag('home/listing.html')
def listing_tag(listing):
  return {'listing':listing}

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.admin.models.category import Category
  categories = {}

  parent_categories = [c for c in Category.objects.all() if c.is_parent_category]
  for parent in parent_categories:
    categories[parent.plural_name] = [sub.plural_name for sub in parent.sub_categories.all()]

  return {'categories': categories}
