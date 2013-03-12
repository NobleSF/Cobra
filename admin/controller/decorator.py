#http://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
#for login: http://www.djangofoo.com/253/writing-django-decorators

from django.shortcuts import redirect
from functools import wraps


def access_required(permission):
  def decorator(func):
    def inner_decorator(request, *args, **kwargs):
      go_for_it = func(request, *args, **kwargs)
      if permission == 'admin' and 'admin_id' in request.session:
        return go_for_it
      elif permission == 'seller' and \
          ('seller_id' in request.session or 'admin id' in request.session):
        return go_for_it
      elif permission == 'account' and 'username' in request.session:
        return go_for_it
      else:
        redirect('login')#, next=go_for_it)
    return wraps(func)(inner_decorator)
  return decorator

def talkative(original_function):
  """
  print a message when original_function starts and finishes
  """
  def new_function(*args, **kwargs):
    print("Entering", original_function.__name__)
    original_function(*args, **kwargs)
    print("Exiting ", original_function.__name__)
  return new_function
