from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
  return render(request, 'seller/home.html')

def edit(request):
  return render(request, 'seller/edit.html')

def asset(request):
  return render(request, 'seller/asset.html')
