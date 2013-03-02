from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator

@decorator.requires_account
def home(request, username):
  return render(request, 'admin/account/home.html')

def create(request, username=None, password=None):
  from admin.models import Account
  from django.db import IntegrityError

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

  if username == None: #coming fresh, just go to the page
    return render(request, 'admin/account/create.html')
  else:
    try:
      new_account = Account(username=username, password=password)
      new_account.save()
      #login(username, password)
      context = {'success': "let's get you logged in"}

    except IntegrityError:
      context = {'problem': "account exists"}
    except Exception as e:
      context = {'exception': e}

    if 'success' in context:
      return login(request, username=username, password=password)
    else:
      return render(request, 'admin/account/create.html', context)

def login(request, username=None, password=None):
  from admin.models import Account
  from admin.controller.forms import AccountLoginForm
  if request.method == 'POST':
    #decrypt_with_private_key()
    form = AccountLoginForm(request.POST)
  elif username is not None and password is not None:
    form = AccountLoginForm(username = username, password = password)

  context = {}
  try:
    if form.is_valid():
      data = form.cleaned_data
      #process the login
      if Account.objects.get(username=username).password == password:
        request.session['username'] = username
        #if seller, set session['seller_pk']
        #if admin, set session['admin_priveledge']
        return redirect('home')
      else:
        context = {'problem': "wrong username"}

  except Account.DoesNotExist:
    context = {'problem': "account does not exist"}

  except Exception as e:
    context = {'exception': e}

  if 'form' not in context: context['form'] = AccountLoginForm()
  #context['public_key'] = create new public key
  return render(request, 'admin/account/login.html', context)

def logout(request, username):
  try:
    del request.session['username']
    context = {'success': "get outta here."}
  except KeyError: # if no one was logged in
    context = {'success': "get outta here."}
  except Exception as e:
    context = {'exception': e}

  if 'success' in context:
    return redirect('home')
  else:
    return render(request, 'public/home.html', context)

@decorator.requires_account
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
