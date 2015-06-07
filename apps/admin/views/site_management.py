from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms.models import modelformset_factory

from apps.admin.utils.decorator import access_required
from apps.public.views.events import invalidate_cache


@access_required('admin')
def rebuildProductRankings(request):
  from apps.public.views.events import rebuildRankings
  rebuildRankings()
  return redirect('home')

@access_required('admin')
def rebuildHomePage(request):
  if (invalidate_cache('home_header') and invalidate_cache('home_content')):
    return redirect('home')
  else:
    messages.error(request,"Error refreshing cache on homepage")
    return redirect('admin:home')

@access_required('admin')
def rebuildProductPage(request=None, product_id=None):
  from apps.public.views.events import invalidate_product_cache
  try:
    invalidate_product_cache(product_id)
  except:
    messages.error(request,"Error refreshing cache on product page")
  return redirect('product', product_id)

@access_required('admin')
def rebuildStorePage(request, seller_id):
  from apps.public.views.events import invalidate_seller_cache
  try:
    invalidate_seller_cache(seller_id)
  except:
    messages.error(request,"Error refreshing cache on store page")
  return redirect('store', seller_id)

@access_required('admin')
def cache(request):
  return render(request, 'site_management/cache.html', {})

@access_required('admin')
def cacheReset(request):
  from apps.public.views.events import invalidateAllProductCaches, invalidateAllSellerCaches
  try:
    if request.method == "GET" and request.GET.get('target', None):
      if request.GET['target'] == 'all product pages':
        invalidateAllProductCaches()
      elif request.GET['target'] == 'all seller pages':
        invalidateAllSellerCaches()
      else:
        raise Exception("invalid target")
    else:
      raise Exception("invalid request")
  except:
    return HttpResponse(status=400)#bad request
  else:
    return HttpResponse(status=200)#OK

@access_required('admin')
def country(request):
  from apps.common.models.country import Country
  CountryFormSet = modelformset_factory(Country, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = CountryFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Country saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CountryFormSet(queryset=Country.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def currency(request):
  from apps.common.models.currency import Currency
  CurrencyFormSet = modelformset_factory(Currency, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = CurrencyFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Currency saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CurrencyFormSet(queryset=Currency.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def color(request):
  from apps.common.models.color import NewColor
  ColorFormSet = modelformset_factory(NewColor, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = ColorFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Color saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ColorFormSet(queryset=NewColor.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def category(request):
  from apps.admin.models.category import Category
  CategoryFormSet = modelformset_factory(Category, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = CategoryFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Category saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CategoryFormSet(queryset=Category.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def ratingSubject(request):
  from apps.admin.models.rating_subject import RatingSubject
  RatingSubjectFormSet = modelformset_factory(RatingSubject, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = RatingSubjectFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Rating Subject saved.')
    except Exception as e:
      messages.error(request, e)
  formset = RatingSubjectFormSet(queryset=RatingSubject.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def shippingOption(request):
  from apps.seller.models.shipping_option import ShippingOption
  ShippingOptionFormSet = modelformset_factory(ShippingOption, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = ShippingOptionFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Shipping Option saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ShippingOptionFormSet(queryset=ShippingOption.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def imageObject(request):
  from apps.seller.models.image import Image
  ImageFormSet = modelformset_factory(Image, exclude=[])
  context = {}
  if request.method == 'POST':
    formset = ImageFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Image Object saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ImageFormSet(queryset=Image.objects.order_by('id').reverse()[:5])
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)
