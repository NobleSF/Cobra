from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from apps.admin.models import Account

@access_required('account')
def home(request):
  return render(request, 'account/home.html')

@access_required('admin')
def create(request):
  from apps.admin.controller.forms import AccountCreateForm
  from django.db import IntegrityError
  from apps.seller.controller.account import create as createSeller

  if request.method == 'POST':
    try:
      username = request.POST.get('username')
      password = process_password(request.POST.get('password'))
      account = Account(username=username, password=password)
      account.is_admin = (request.POST['account_type'] == 'admin')
      account.save()

      if account.is_admin:
        messages.success(request, 'Admin account created.')

      else: #seller account
        if createSeller(account) == True:
          #messages.success(request, 'Seller account created.')
          login(request)
          return redirect('seller:edit')
        else:
          messages.error(request, 'Error creating seller account.')
          error_message = createSeller(account)
          messages.error(request, error_message)
          account.delete()

    except IntegrityError:
      messages.warning(request, 'An account with this username already exists.')
    except Exception as e:
      messages.error(request, e)

  context = {'form': AccountCreateForm()}
  return render(request, 'account/create.html', context)

@access_required('admin')
def all_accounts(request):
  context = {'accounts':Account.objects.order_by('is_admin','name')}
  return render(request, 'account/all_accounts.html', context)

@access_required('admin')
def edit(request, account_id=None):
  from apps.admin.controller.forms import AccountEditForm
  account = Account.objects.get(
    id = request.session.get('admin_id')
  )
  form = AccountEditForm()
  return render(request, 'account/edit.html', {'form': form})

def login(request, next=None):
  from apps.admin.controller.forms import AccountLoginForm
  from apps.seller.models import Seller

  if request.method == 'POST':
    form = AccountLoginForm(request.POST)
    try:
      account = None
      username = request.POST['username']
      password = process_password(request.POST['password'])

      #login with phone number
      if not account:
        try:
          l = len(username)
          account = Account.objects.get(phone__endswith=username[l-8:l])
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

      #lower-case first letter (for phones that auto-capitalize it)
      username_as_list = list(username)
      username_as_list[0] = username_as_list[0].lower()
      username = "".join(username_as_list)
      if not account:
        try: account = Account.objects.get(username=username)
        except: pass
        try: account = Account.objects.get(email=username)
        except: pass

      if account and account.password == password:

        if account.is_admin:
          request.session['admin_id'] = account.id
          request.session['username'] = account.username
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
      context = {'exception': e}

    context['form'] = AccountLoginForm()#return fresh form

  else:
    if next:
      request.session['next'] = next #path of requested page after login
    context = {'form': AccountLoginForm()}

  #context['public_key'] = create new public key
  return render(request, 'account/login.html', context)

def logout(request):
  try:
    if 'username' in request.session: del request.session['username']
    if 'admin_id' in request.session: del request.session['admin_id']
    if 'seller_id' in request.session: del request.session['seller_id']
    return redirect('home')
  except Exception as e:
    context = {'exception': e}
    return render(request, 'public/home.html', context)

@access_required('account')
def password(request, username, new_password, secret_hash="", old_password=""):
  from apps.admin.models import Account

  if request.method == 'POST':
    username = request.POST['username']
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']

  if request.method == 'GET':
    username = request.GET['username']
    secret_hash = request.GET['secret_hash']
    new_password = request.GET['new_password']

  # if any of the necessary information is missing
  if username == None or new_password == None:

    if request.method == 'GET' and secret_hash != "": #came from email link
      context = {'secret_hash': secret_hash}
      return render(request, 'account/password.html', context)
    else: #coming fresh, just go to the page
      #reset secret_hash, just in case
      return render(request, 'account/password.html')

  elif old_password != "":
    try:
      this_account = Account.objects.get(username=username)
      if this_account.password == old_password:
        this_account.password = new_password
        this_account.save()
        #reset secret_hash, just in case
        context = {'success': "password has been changed"}
      else:
        context = {'problem': "old password incorrect"}
    except Exception as e:
      context = {'exception': e}

    #todo: don't allow password to be same as username

  elif secret_hash != "":
    try:
      this_account = Account.objects.get(username=username)
      if this_account.secret_hash == secret_hash:
        this_account.password = new_password
        this_account.save()
        #reset secret_hash, just in case
        context = {'success': "password has been changed"}
      else:
        context = {'problem': "secret hash out of date"}
    except Exception as e:
      context = {'exception': e}

  else:
    context = {'problem': "issue submitted to the Vogon bureaucracy"}

  #success or not, take them back where they came from.
  return render(request, 'account/password.html', context)

def process_password(encrypted): #private function
  from Crypto.Hash import SHA256
  #http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
  #https://www.dlitz.net/software/pycrypto/doc/
  decrypted = encrypted #decrypt with private key
  hashed = SHA256.new(decrypted).hexdigest()
  return hashed
