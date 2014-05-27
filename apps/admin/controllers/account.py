from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.contrib import messages
import json
from django.utils import timezone
from datetime import timedelta
from apps.admin.models import Account

@access_required('admin')
def adminAccounts(request):
  from django.db.models import Count
  #types_order = ['unassigned', 'translator', 'trainer', 'country', 'master']
  admin_accounts = (Account.objects
                    .annotate(num_sellers=Count('sellers'))
                    .filter(
                      admin_type__isnull=False,
                      num_sellers=0)
                    #.exclude(admin_type='master')
                    .order_by('admin_type', 'name'))

  return render(request, 'account/admin_accounts.html', {'accounts':admin_accounts})

@access_required('admin')
def createAdmin(request):
  from apps.admin.controllers.forms import AccountCreateForm
  from django.db import IntegrityError

  if request.method == 'POST':

    name        = request.POST.get('name')
    phone       = request.POST.get('phone')
    password    = request.POST.get('password')
    password    = processPassword(password) if password else None
    admin_type  = request.POST.get('admin_type')

    if not phone:
      context = {'incorrect': "bad phone"}
    elif not password:
      context = {'incorrect': "bad password"}
    elif not admin_type:
      context = {'incorrect': "bad admin_type"}

    else:
      try:
        account = Account(phone=phone, password=password, admin_type=admin_type)
        account.name = name if name else None
        account.save()
        return redirect('admin:edit account', account.id)

      except IntegrityError:
        messages.warning(request, 'An account with this phone already exists.')
        context = {'incorrect': "bad phone"}

      except Exception as e:
        ExceptionHandler(e, "in account.createAdmin")
        messages.error(request, e)

  else:
    context = {}

  context['form'] = AccountCreateForm()
  return render(request, 'account/create_admin.html', context)

@access_required('admin')
def sellerAccounts(request):
  from django.db.models import Count
  seller_accounts = (Account.objects
                     .annotate(num_sellers=Count('sellers'))
                     .filter(
                      admin_type__isnull=True,
                      num_sellers=1))
  seller_accounts = sorted(seller_accounts, key=lambda a: a.sellers.all()[0].city)

  return render(request, 'account/seller_accounts.html', {'accounts':seller_accounts})

@access_required('admin')
def createSeller(request):
  from apps.admin.controllers.forms import AccountCreateForm
  from django.db import IntegrityError
  from apps.seller.controllers.account import create as createSeller
  context = {}

  if request.method == 'POST':

    name        = request.POST.get('name')
    phone       = request.POST.get('phone')
    password    = request.POST.get('password')
    password    = processPassword(password) if password else None

    if not phone and phone.isdigit():
      context = {'incorrect': "bad phone"}
    elif not password:
      context = {'incorrect': "bad password"}

    else:
      try:
        account = Account(phone=phone, password=password)
        account.name = name if name else None
        account.save()

        if createSeller(account):
          login(request)
          return redirect('seller:edit')
        else:
          e = Exception("createSeller() returned False")
          ExceptionHandler(e, 'in account.createSeller')
          messages.error(request, 'Error creating seller account.')
          account.delete()

      except IntegrityError:
        messages.warning(request, 'An account with this phone already exists.')
        context = {'incorrect': "bad phone"}

      except Exception as e:
        ExceptionHandler(e, "in account.createSeller")
        messages.error(request, e)

  context['form'] = AccountCreateForm()
  return render(request, 'account/create_seller.html', context)

@access_required('admin')
def edit(request, account_id=None):
  from apps.admin.controllers.forms import AccountEditForm

  if not account_id:
    account_id = request.session.get('admin_id')
  account = Account.objects.get(id=account_id)

  if request.method == 'POST':
    account_model_form = AccountEditForm(request.POST, instance=account)
    if account_model_form.is_valid():
      account_model_form.save()
      if account.is_admin:
        return redirect('admin:admin accounts')
      else:#seller
        return redirect('admin:seller accounts')
    else:
      messages.warning(request, 'Not saved. Some data is invalid.')

  else:
    account_model_form = AccountEditForm(instance=account)

  context = {'account':account, 'form':account_model_form}

  return render(request, 'account/edit.html', context)

@access_required('admin')
def approveSeller(request): #from AJAX GET request
  from apps.seller.models.seller import Seller
  try:
    seller_id = request.GET['seller_id']
    action = request.GET['action']
    seller = Seller.objects.get(id=seller_id)
    if action == 'approve':
      seller.approved_at = timezone.now()
      seller.save()

      #reapprove all seller products that were approved in the last 14 days
      fourteen_days_ago = timezone.now() - timedelta(days=14)
      for product in (seller.product_set
                      .filter(approved_at__lte=timezone.now())
                      .exclude(approved_at__lte=fourteen_days_ago)):
        product.approved_at = timezone.now()
        product.save()

    elif action == 'unapprove':
      seller.approved_at = None
      seller.save()
      #todo: refresh homepage cache
    elif action == 'delete':
      seller.delete();
    else:
      raise Exception('invalid action: %s' % action)
  except Exception as e:
    ExceptionHandler(e, "error on seller approval")
    response = {'error': str(e)}
  else:
    response = {'success': "%s %s" % (action, seller_id)}

  return HttpResponse(json.dumps(response), content_type='application/json')

def login(request, next=None):
  from apps.admin.controllers.forms import AccountLoginForm
  from apps.seller.models.seller import Seller

  if request.method == 'POST':
    form = AccountLoginForm(request.POST)
    try:
      account = None
      username = request.POST.get('username', '')
      if not username:
        username = request.POST.get('phone', '')

      #login with phone number
      if not account:
        try:
          account = Account.objects.get(phone__endswith=username[-8:])#last 8 chars
        except: pass

      #login with username
      if not account:
        try:
          account = Account.objects.get(username=username)
        except: pass

      #login with email address
      if not account:
        try:
          account = Account.objects.get(email=username)
        except: pass

      if not account:
        #lower-case first letter (for phones that auto-capitalize it)
        if len(username) > 0:
          username_as_list = list(username)
          username_as_list[0] = username_as_list[0].lower()
          username = "".join(username_as_list)

        try:
          account = Account.objects.get(username=username)
        except:
          try:
            account = Account.objects.get(email=username)
          except: pass

      if account and account.password == processPassword(request.POST.get('password', '')):

        if account.is_admin:
          request.session['admin_id'] = account.id
          request.session['admin_type'] = account.admin_type
          request.session['username'] = account.username
          if 'cart_id' in request.session:
            del request.session['cart_id']

        else:#is seller
          try:
            seller = Seller.objects.get(account_id=account.id)
          except Seller.DoesNotExist:
            seller = None
          else:
            request.session['seller_id'] = seller.id

        if 'username' not in request.session: #keep admin username if already logged in
          request.session['username'] = account.username

        if 'next' in request.session:
          full_path = request.session['next']
          del request.session['next']
          return HttpResponseRedirect(full_path)
        else:
          return redirect('seller:home')

      elif not account:
        context = {'incorrect': "wrong username"}
      else:
        context = {'incorrect': "wrong password"}

    except Exception as e:
      ExceptionHandler(e, "error in login function")
      context = {'exception': e}

    context['form'] = AccountLoginForm()#return fresh form

  else:
    if next:
      request.session['next'] = next #path of requested page after login
    context = {'form': AccountLoginForm()}

  #context['public_key'] = create new public key
  return render(request, 'account/login.html', context)

@access_required('admin')
def loginCheat(request):
  from apps.seller.models.seller import Seller

  seller_id = request.GET.get('seller_id')
  destination = request.GET.get('destination')

  request.session['seller_id'] = seller_id
  return HttpResponseRedirect(destination)


def logout(request):
  try:
    for var in ['username', 'admin_id', 'admin_type', 'seller_id', 'cart_id', 'next']:
      if var in request.session:
        del request.session[var]

  except Exception as e:
    ExceptionHandler(e, "error in logout function")

  finally:
    return redirect('home')

@access_required('admin')
def resetPassword(request, account_id=None):
  from apps.admin.controllers.forms import AccountPasswordForm
  account_id = account_id if account_id else request.session.get('admin_id')
  account = Account.objects.get(id=account_id)

  if request.method == 'POST':
    try:
      new_password = processPassword(request.POST.get('new_password'))
      account.password = new_password
      account.save()
      if account.is_admin:
        return redirect('admin:edit account', account.id)
      else:#seller
        return redirect('seller:edit')

    except Exception as e:
      ExceptionHandler(e, "error on password reset")
      messages.warning(request, str(e))

  context = {'form':AccountPasswordForm(), 'account_name':account.name}
  return render(request, 'account/reset_password.html', context)

def processPassword(encrypted): #private function
  from Crypto.Hash import SHA256
  #http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
  #https://www.dlitz.net/software/pycrypto/doc/
  decrypted = encrypted #decrypt with private key
  hashed = SHA256.new(decrypted).hexdigest()
  return hashed
