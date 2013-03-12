from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller.decorator import access_required

@access_required('account')
def home(request, username):
  return render(request, 'admin/account/home.html')

@access_required('admin') #why do customers need accounts?
def create(request):
  from admin.controller.forms import AccountCreateForm
  from admin.models import Account
  from django.db import IntegrityError

  if request.method == 'POST':
    form = AccountCreateForm(request.POST)
    if form.is_valid():
      try:
        form.save()
        return login(request)

      except IntegrityError:
        context = {'problem': "account exists"}
      except Exception as e:
        context = {'exception': e}

    else:
      context = {'problem': "invalid data"}

  else:
    context = {}
    form = AccountCreateForm()

  context['form'] = form
  return render(request, 'admin/account/create.html', context)

@access_required('account')
def edit(request):
  from admin.controller.forms import AccountEditForm
  form = AccountEditForm()

  return render(request, 'admin/account/edit.html', {'form': form})

def login(request, next=None):
  from admin.models import Account
  from admin.controller.forms import AccountLoginForm
  if request.method == 'POST':
    form = AccountLoginForm(request.POST)
    try:
        username = request.POST['username']
        password = process_password(request.POST['password'])
        account = Account.objects.get(username=username)
        if account.password == password:
          request.session['username'] = username
          if account.is_admin:
            request.session['admin_id'] = account.id
          #if seller, set session['seller_id']
          if next is not None:
            return next
          else:
            return redirect('home')
        else:
          context = {'problem': "wrong password"}

    except Account.DoesNotExist:
      context = {'problem': "account does not exist"}
    except Exception as e:
      context = {'exception': e}
    #context['form'] = AccountLoginForm()#return fresh form

  else:
    context = {'form': AccountLoginForm()}

  #context['public_key'] = create new public key
  return render(request, 'admin/account/login.html', context)

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
  from admin.models import Account

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
      return render(request, 'admin/account/password.html', context)
    else: #coming fresh, just go to the page
      #reset secret_hash, just in case
      return render(request, 'admin/account/password.html')

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
  return render(request, 'admin/account/password.html', context)

def process_password(encrypted): #private function
  from Crypto.Hash import SHA256
  #http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
  #https://www.dlitz.net/software/pycrypto/doc/
  decrypted = encrypted #decrypt with private key
  hashed = SHA256.new(decrypted).hexdigest()
  return hashed
