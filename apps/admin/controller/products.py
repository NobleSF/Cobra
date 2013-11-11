from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.utils import simplejson, timezone
from apps.seller.models import Product
from settings.people import Tom
from apps.communication.controller.email_class import Email

@access_required('admin')
def product_lookup(request):
  context = {}
  if request.method == "POST":
    try:
      product = Product.objects.get(id=request.POST.get('product_id'))
      product.artisan = product.assets.filter(ilk='artisan')[0]
      product.materials = product.assets.filter(ilk='material')
      product.tools     = product.assets.filter(ilk='tool')
      context['product'] = product

    except Product.DoesNotExist:
      context['problem'] = "No Product with that ID"
    except Exception as e:
      context['problem'] = str(e)
  return render(request, 'products/product_lookup.html', context)

@access_required('admin')
def review_products(request):
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
def unrated_products(request):
  from django.db.models import Count
  unrated_products = (Product.objects.filter(in_holding=False,
                                             active_at__lte=timezone.now(),
                                             deactive_at=None,
                                             sold_at=None)
                      .annotate(rating_count=Count('rating'))
                      .filter(rating_count__lt=15)
                      .exclude(rating__session_key = request.session.session_key))

  return render(request, 'products/unrated_products.html', {'products':unrated_products})

@access_required('admin')
def approve_product(request): #from AJAX GET request
  from apps.seller.models import Product
  try:
    product_id = request.GET['product_id']
    action = request.GET['action']
    product = Product.objects.get(id=product_id)
    if action == 'approve':
      product.in_holding = False
      product.approved_at = timezone.now()
      product.save()
    elif action == 'hold':
      product.approved_at = None
      product.in_holding = True
      product.save()
    elif action == 'delete':
      product.delete();
    else:
      raise Exception('invalid action: %s' % action)
  except Exception as e:
    response = {'error': str(e)}
    Email(message="error on product approval: "+str(e)).sendTo(Tom.email)
  else:
    response = {'success': "%s %s" % (action, product_id)}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@access_required('admin')
def rate_product(request): #from AJAX GET request
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
    response = {'error': e}
    Email(message="error in rate_product function: "+str(e)).sendTo(Tom.email)
  else:
    response = {'success': "%s rated" % product_id}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
