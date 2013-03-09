#http://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
from django.shortcuts import redirect

def requires_account(function):
  """
  1 verify user is logged in
  2 if not, send to login
  """
  if 'username' in request.session:
    return function
  else:
    context = {'problem': "Login Required", 'next':request}
    return redirect('login', context)

def requires_seller_or_admin(function):
  """
  1 verify user is a seller or admin
  2 if not logged in, send to login
  3 if not seller or admin, deny access
  """
  if 'admin_pk' in request.session or 'seller_pk' in request.session:
    return function
  elif 'username' not in request.session:
    context = {'problem': "Login Required", 'next':request}
    return redirect('login', context)
  else:
    context = {'problem': "Access Denied"}
    return redirect('home', context)

def requires_admin(function):
  """
  1 verify user is an admin
  2 if not logged in, send to login
  3 if not admin, deny access
  """
  if 'admin_pk' in request.session:
    return function
  elif 'username' not in request.session:
    context = {'problem': "Login Required", 'next':request}
    return redirect('login', context)
  else:
    context = {'problem': "Access Denied"}
    return redirect('home', context)

def talkative(original_function):
  """
  print a message when original_function starts and finishes
  """
  def new_function(*args, **kwargs):
    print("Entering", original_function.__name__)
    original_function(*args, **kwargs)
    print("Exiting ", original_function.__name__)
  return new_function
