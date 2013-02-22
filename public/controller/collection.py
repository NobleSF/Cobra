from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, group, id=None):
  return render(request, 'public/collection.html',
    {'group':group}
  )
