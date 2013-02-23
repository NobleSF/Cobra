from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request):
  return render(request, 'public/home/home.html')

def about(request):
  return render(request, 'public/home/about.html')

def faq(request):
  return render(request, 'public/home/faq.html')

def contact(request):
  return render(request, 'public/home/contact.html')
