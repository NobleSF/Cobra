from django.shortcuts import render, redirect
from apps.admin.controller.decorator import access_required
from django.contrib import messages

@access_required('admin')
def dashboard(request):
  return render(request, 'dashboard.html')
