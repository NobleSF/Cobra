from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler


@access_required('seller')
def home(request):
  from apps.seller.models.seller import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    context = {'seller': seller}
  except Exception as e:
    ExceptionHandler(e, "in seller.home")
    context = {'exception': e}

  return render(request, 'seller_home.html', context)
