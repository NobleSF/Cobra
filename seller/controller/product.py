from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
  return render(request, 'seller/product/home.html')

def create(request):
  #create product object and send to edit function
  return render(request, 'seller/product/edit.html')

def detail(request, id):
  return render(request, 'seller/product/detail.html')

def edit(request, id):
  return render(request, 'seller/product/edit.html')

def delete(request, id):
  #archive product and return to product home
  return render(request, 'seller/product/home.html')
