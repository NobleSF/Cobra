from django.contrib.sitemaps import Sitemap
from apps.seller.models import Seller, Product
from django.utils import timezone
from django.core.urlresolvers import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'blog']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
  changefreq = "daily"
  priority = 0.6 #use product rating here? range [.4:1]

  def items(self):
    return Product.objects.filter(active_at__lte=timezone.now(),
                                  in_holding=False,
                                  deactive_at=None)

  def lastmod(self, item):
    return item.updated_at

class StoreSitemap(Sitemap):
  changefreq = "daily"
  priority = 0.6

  def items(self):
    return Seller.objects.filter(approved_at__lte=timezone.now(),
                                 deactive_at=None)

  def lastmod(self, item):
    return item.updated_at

sitemaps = {
  'static':   StaticViewSitemap,
  'products': ProductSitemap,
  'stores':   StoreSitemap
}
