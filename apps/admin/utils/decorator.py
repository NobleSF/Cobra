#http://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
#for login: http://www.djangofoo.com/253/writing-django-decorators

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from functools import wraps

def access_required(permission):
  def decorator(func):
    def inner_decorator(request, *args, **kwargs):

      if (permission == 'admin' and
          'admin_id' in request.session):
        return func(request, *args, **kwargs)

      elif (permission == 'admin or seller' and
            ('admin_id' in request.session or
             'seller_id' in request.session)):
        return func(request, *args, **kwargs)

      elif (permission == 'seller' and
            'seller_id' in request.session):
        return func(request, *args, **kwargs)

      elif permission == 'account' and 'username' in request.session:
        return func(request, *args, **kwargs)

      else:
        from apps.admin.controllers.account import login
        return login(request, next=request.get_full_path())

    return wraps(func)(inner_decorator)
  return decorator


# A DECORATOR FOR PYTHON THREADING
# http://docs.python.org/2/library/threading.html#thread-objects

from threading import Thread

def postpone(function):
  def decorator(*args, **kwargs):
    t = Thread(target = function, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()

  return decorator
