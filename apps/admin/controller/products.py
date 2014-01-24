from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.utils.decorator import access_required
from django.contrib import messages
from apps.admin.utils.exception_handling import ExceptionHandler
from django.forms.models import modelformset_factory
from django.utils import timezone
import json
from apps.seller.models import Product

@access_required('admin')
def productLookup(request):
  context = {}
  if request.method == "POST":
    try:
      product = Product.objects.get(id=request.POST.get('product_id'))

    except Product.DoesNotExist:
      context['problem'] = "No Product with that ID"
    except Exception as e:
      context['problem'] = str(e)
  return render(request, 'products/product_lookup.html', {'product':product})

@access_required('admin')
def reviewProducts(request):
  products_to_review = (Product.objects.filter(approved_at=None,
                                               active_at__lte=timezone.now(),
                                               deactive_at=None,
                                               sold_at=None,
                                               in_holding=False)
                        .order_by('updated_at'))

  products_in_holding = (Product.objects.filter(in_holding=True,
                                                active_at__lte=timezone.now(),
                                                deactive_at=None,
                                                sold_at=None)
                        .order_by('updated_at'))

  context = {'products_to_review': products_to_review,
             'products_in_holding': products_in_holding
            }
  return render(request, 'products/review_products.html', context)

@access_required('admin')
def unratedProducts(request):
  from django.db.models import Count
  unrated_products = (Product.objects.filter(in_holding=False,
                                             active_at__lte=timezone.now(),
                                             deactive_at=None,
                                             sold_at=None)
                      .annotate(rating_count=Count('rating'))
                      .filter(rating_count__lt=15)
                      .exclude(rating__session_key=request.session.session_key)[:50])

  return render(request, 'products/unrated_products.html', {'products':unrated_products})

@access_required('admin')
def approveProduct(request): #from AJAX GET request
  from apps.seller.controller.product_class import Product
  try:
    product = Product(request.GET.get('product_id'))
    action = request.GET.get('action')

    if action == 'approve':
      product.approve()
    elif action == 'hold':
      product.hold()
    elif action == 'delete':
      product.delete();
    else:
      raise Exception('invalid action: %s' % action)
  except Exception as e:
    ExceptionHandler(e, "error on approve_product")
    response = {'error': str(e)}
  else:
    response = {'success': "%s %s" % (action, product.product.id)}

  return HttpResponse(json.dumps(response), content_type='application/json')

@access_required('admin')
def rateProduct(request): #from AJAX GET request
  from apps.seller.models import Product
  from apps.public.models import Rating
  from apps.admin.models import RatingSubject
  try:
    product_id      = request.GET.get('product_id')
    rating_subject  = request.GET.get('subject')
    rating_value    = request.GET.get('value')

    rating_subject_object = RatingSubject.objects.get(name=rating_subject)

    rating = Rating.objects.filter(
              session_key=request.session.session_key,
              subject=rating_subject_object,
              product_id=product_id
            )
    if rating:
      rating[0].value = rating_value
      rating[0].save()
    else:
      rating = Rating(
                  session_key=request.session.session_key,
                  subject=rating_subject_object,
                  product_id=product_id,
                  value = rating_value
                )
      rating.save()

  except Exception as e:
    ExceptionHandler(e, "error on rate_product")
    response = {'error': str(e)}
  else:
    response = {'success': "%s rated" % product_id}

  return HttpResponse(json.dumps(response), content_type='application/json')


def priceCalc(request):
  from apps.admin.models import Currency
  exchange_rate = Currency.objects.get(code='MAD').exchange_rate_to_USD
  return render(request, 'products/price_calc.html', {'exchange_rate':exchange_rate})
