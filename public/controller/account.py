from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def create(request, username=None, password=None):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

  if username == None:
    return render(request, 'public/account/create.html')
  else:
    try:
      new_account = Account.create(username=username, password=password)
      #login(username, password)

    except:
      return render(request, 'public/account/create.html', {
        'error': 'could not process request',
      })

def login(request, username=None, password=None):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

  if username == None:
    return render(request, 'public/account/login.html')

def logout(request, username):
  return render(request, 'public/account/logout.html',
    {'username':username}
  )

def home(request, username):
  return render(request, 'public/account/home.html',
    {'username':username}
  )
