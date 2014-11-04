from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models.seller import Seller
from apps.seller.models.product import Product

@access_required('seller')
def products(request):
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = (seller.product_set.filter(active_at__lte=timezone.now(),
                                          deactive_at=None,
                                          sold_at=None))

    #unapproved_products = products.filter(Q(approved_at__lte=timezone.now()) |
    #                                      Q(in_holding=True))

    context = {'seller': seller, 'products': products}
  except Exception as e:
    ExceptionHandler(e, "in seller.products")
    context = {'exception': e}

  return render(request, 'inventory/products.html', context)

@access_required('seller')
def orders(request):
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    sold_products = seller.product_set.filter(sold_at__lte=timezone.now())
    for product in sold_products:
      product.order = product.order_set.all()[0]
    context = {'seller': seller, 'products': sold_products}

  except Exception as e:
    ExceptionHandler(e, "in seller.products")
    context = {'exception': e}

  return render(request, 'inventory/orders.html', context)

@access_required('seller')
def create(request):
  seller = Seller.objects.get(id=request.session['seller_id'])
  checkInventory(seller)
  try:
    product_to_edit = None
    for product in seller.product_set.all().order_by('id'):
      if not product_to_edit and product.was_never_active:
        product_to_edit = product

    if not product_to_edit:
      product_to_edit = Product(seller=seller)
      product_to_edit.save()

    return redirect('seller:edit product', product_id=product_to_edit.id)

  except Exception as e:
    ExceptionHandler(e, "in inventory.create")
    return redirect('seller:home')

@access_required('seller')
def remove(request, product_id): #seller deactivate product #todo: merge logic with saveProduct
  try:
    product = Product.objects.get(id=product_id,
                                  seller_id=request.session['seller_id'])
    product.is_active = False
    product.save()

    if request.session.get('admin_id'):
      messages.success(request, "Product successfully removed from inventory.")

  except Exception as e:
    ExceptionHandler(e, "in inventory.remove")
    if request.session.get('admin_id'):
      messages.warning(request, "Unable to remove product.")

  return redirect('seller:products')

def checkInventory(seller):
  #preferred method
  #inactive_products = seller.product_set.filter('is_active' = False)
  #if len(inactive_products) > 1:
  #  inactive_products[1:].delete()

  #hacked method: keep first inactive, else delete
  try:
    keep = 1
    for product in seller.product_set.all().order_by('id'):
      if product.was_never_active:
        if keep <= 0:
          #product.delete()
          e = Exception('Seller has multiple products in edit process.')
          ExceptionHandler(e, "in inventory.checkInventory")
        keep -= 1
  except Exception as e:
    ExceptionHandler(e, "in inventory.checkInventory")
    return False
  else:
    return True
