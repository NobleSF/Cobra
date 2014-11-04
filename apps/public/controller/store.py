from django.shortcuts import render, redirect, get_object_or_404
from apps.seller.models.seller import Seller

def home(request, seller_id, slug=None):
  store = get_object_or_404(Seller, id=seller_id)

  #permanent redirect when slug not included
  if store.slug and slug != store.slug:
    return redirect(store, permanent=True) #uses get_absolute_url

  return render(request, 'store.html', {'store':store})
