#http://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/

def requires_account(function):
  """
  1 verify user is logged in
  2 if not, send to login
  """
  return function

def requires_seller_or_admin(function):
  """
  1 verify user is a seller
  2 if not and not logged in, send to login
  3 if not and are logged in, deny access
  """
  return function

def requires_admin(function):
  """
  1 verify user is an admin
  2 if not and not logged in, send to login
  3 if not and are logged in, deny access
  """
  return function


def talkative(original_function):
  """
  print a message when original_function starts and finishes
  """
  def new_function(*args, **kwargs):
    print("Entering", original_function.__name__)
    original_function(*args, **kwargs)
    print("Exiting ", original_function.__name__)
  return new_function
