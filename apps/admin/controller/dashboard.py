from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.controller.decorator import access_required
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime

@access_required('admin')
def home(request):
  return render(request, 'dashboard/home.html')

@access_required('admin')
def review_products(request):
  from apps.seller.models import Product
  new_products = Product.objects.filter(active_at__lte=datetime.today())
  yet_approved = new_products.filter(approved_at=None)
  products_to_review = yet_approved.order_by('updated_at').reverse()

  context = {'products': products_to_review}
  return render(request, 'dashboard/review_products.html', context)

@access_required('admin')
def approve_product(request):
  from apps.seller.models import Product
  try:
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    product.approved_at = datetime.now()
    product.save()
  except Exception as e:
    response = {'exception': e}
  else:
    response = {'success': str(product.id) + " approved"}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@access_required('admin')
def country(request):
  from apps.admin.models import Country
  CountryFormSet = modelformset_factory(Country)
  context = {}
  if request.method == 'POST':
    formset = CountryFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = CountryFormSet(queryset=Country.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def currency(request):
  from apps.admin.models import Currency
  CurrencyFormSet = modelformset_factory(Currency)
  context = {}
  if request.method == 'POST':
    formset = CurrencyFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = CurrencyFormSet(queryset=Currency.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def color(request):
  from apps.admin.models import Color
  ColorFormSet = modelformset_factory(Color)
  context = {}
  if request.method == 'POST':
    formset = ColorFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = ColorFormSet(queryset=Color.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def category(request):
  from apps.admin.models import Category
  CategoryFormSet = modelformset_factory(Category)
  context = {}
  if request.method == 'POST':
    formset = CategoryFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = CategoryFormSet(queryset=Category.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def rating_subject(request):
  from apps.admin.models import RatingSubject
  RatingSubjectFormSet = modelformset_factory(RatingSubject)
  context = {}
  if request.method == 'POST':
    formset = RatingSubjectFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = RatingSubjectFormSet(queryset=RatingSubject.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def shipping_option(request):
  from apps.seller.models import ShippingOption
  ShippingOptionFormSet = modelformset_factory(ShippingOption)
  context = {}
  if request.method == 'POST':
    formset = ShippingOptionFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = ShippingOptionFormSet(queryset=ShippingOption.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)

@access_required('admin')
def image_object(request):
  from apps.seller.models import Image
  ImageFormSet = modelformset_factory(Image)
  context = {}
  if request.method == 'POST':
    formset = ImageFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  formset = ImageFormSet(queryset=Image.objects.all())
  context['formset'] = formset
  return render(request, 'dashboard/formset.html', context)
