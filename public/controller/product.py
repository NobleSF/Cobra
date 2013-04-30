from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, id):
  return render(request, 'product.html',
    {'id':id}
  )

def collection(request, group, name=None):
  return render(request, 'collection.html',
    {'group':group}
  )
