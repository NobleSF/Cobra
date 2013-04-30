from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, id):
  return render(request, 'product/detail.html',
    {'id':id}
  )

def collection(request, group, name=None):
  return render(request, 'product/collection.html',
    {'group':group}
  )
