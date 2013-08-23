from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.utils import simplejson
from datetime import datetime

@access_required('admin')
def review_products(request):
  from apps.seller.models import Product
  from apps.admin.models import RatingSubject

  new_products = Product.objects.filter(active_at__lte=datetime.today())
  yet_approved = new_products.filter(approved_at=None)
  products_to_review = yet_approved.order_by('updated_at').reverse()

  for product in products_to_review:
    product.admin_ratings = product.rating_set.filter(session_key = request.session.session_key)

  rating_subjects = RatingSubject.objects.all()

  context = {'products': products_to_review,
             'rating_subjects': rating_subjects,
             'rating_values': range(0,6)
            }
  return render(request, 'products/review_products.html', context)

@access_required('admin')
def approve_product(request): #from AJAX GET request
  from apps.seller.models import Product
  try:
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    product.approved_at = datetime.now()
    product.save()
  except Exception as e:
    response = {'error': e}
  else:
    response = {'success': "%d approved" % product.id}

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
  else:
    response = {'success': "%s rated" % product_id}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
