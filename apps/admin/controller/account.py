from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.contrib import messages
from django.utils import simplejson, timezone
from datetime import timedelta
from apps.admin.models import Account

@access_required('admin')
def create(request):
  from apps.admin.controller.forms import AccountCreateForm
  from django.db import IntegrityError
  from apps.seller.controller.account import create as createSeller

  if request.method == 'POST':
    try:
      if request.POST.get('username') and request.POST.get('password'):
        username = request.POST.get('username')
        password = process_password(request.POST.get('password'))
        account = Account(username=username, password=password)
        account.save()

        if request.POST['account_type'] == 'admin':
          account.admin_type = "unassigned"
          account.save()
          messages.success(request, 'Admin account created. Ask Tom to set admin privileges')
          return redirect('admin:account edit', account.id)

        else: #seller account
          if createSeller(account):
            login(request)
            return redirect('seller:edit')
          else:
            messages.error(request, 'Error creating seller account.')
            account.delete()

      else:
        messages.warning(request, 'Missing username and/or password')

    except IntegrityError:
      messages.warning(request, 'An account with this username already exists.')
    except Exception as e:
      ExceptionHandler(e, "error creating account")
      messages.error(request, e)

  context = {'form': AccountCreateForm()}
  return render(request, 'account/create.html', context)

@access_required('admin')
def all_accounts(request):
  context = {
      'seller_accounts':Account.objects.filter(admin_type__isnull=True).order_by('name')
      #todo: query filter should check for attached seller accounts
    }
  return render(request, 'account/all_accounts.html', context)

@access_required('admin')
def edit(request, account_id=None):
  from apps.admin.controller.forms import AccountEditForm

  if not account_id:
    account_id = request.session.get('admin_id')
  account = Account.objects.get(id=account_id)

  if request.method == 'POST':
    account_model_form = AccountEditForm(request.POST, instance=account)
    if account_model_form.is_valid():
      account_model_form.save()
      messages.success(request, 'Account information saved.')
    else:
      messages.warning(request, 'Not saved. Some data is invalid.')

  else:
    account_model_form = AccountEditForm(instance=account)

  context = {'account':account, 'form':account_model_form}

  return render(request, 'account/edit.html', context)

@access_required('admin')
def approve_seller(request): #from AJAX GET request
  from apps.seller.models import Seller
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

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def login(request, next=None):
  from apps.admin.controller.forms import AccountLoginForm
  from apps.seller.models import Seller

  if request.method == 'POST':
    form = AccountLoginForm(request.POST)
    try:
      account = None
      username = request.POST.get('username', '')

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

      if account and account.password == process_password(request.POST.get('password', '')):

        if account.is_admin:
          request.session['admin_id'] = account.id
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
          return redirect('seller:management home')

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
def login_cheat(request):
  from apps.seller.models import Seller

  seller_id = request.GET.get('seller_id')
  destination = request.GET.get('destination')

  request.session['seller_id'] = seller_id
  return HttpResponseRedirect(destination)


def logout(request):
  try:
    if 'username'   in request.session: del request.session['username']
    if 'admin_id'   in request.session: del request.session['admin_id']
    if 'seller_id'  in request.session: del request.session['seller_id']
    if 'next'       in request.session: del request.session['next']
    if 'cart_id'    in request.session: del request.session['cart_id']

    return redirect('home')

  except Exception as e:
    ExceptionHandler(e, "error in logout function")
    return render(request, 'public/home.html', {'exception':e})

@access_required('admin')
def reset_password(request, account_id=None):
  from apps.admin.controller.forms import AccountPasswordForm
  try:
    account = Account.objects.get(id=account_id)

    if request.method == 'POST':
      #old_password = process_password(request.POST.get('old_password'))
      new_password = process_password(request.POST.get('new_password'))
      account.password = new_password
      account.save()
      messages.success(request, "password changed for %s" % account.name)
      return redirect('admin:account edit', account.id)

  except Exception as e:
    ExceptionHandler(e, "error on password reset")
    messages.warning(request, "invalid passwords provided")

  context = {'form':AccountPasswordForm()}
  #success or not, take them back where they came from.
  return render(request, 'account/reset_password.html', context)

def process_password(encrypted): #private function
  from Crypto.Hash import SHA256
  #http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
  #https://www.dlitz.net/software/pycrypto/doc/
  decrypted = encrypted #decrypt with private key
  hashed = SHA256.new(decrypted).hexdigest()
  return hashed
