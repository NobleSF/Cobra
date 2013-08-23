from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from datetime import datetime

@access_required('admin')
def dashboard(request):
  return render(request, 'dashboard.html')
