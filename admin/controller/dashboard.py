from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator
from django.forms.models import modelformset_factory

def home(request):
  return render(request, 'public/home.html')

def country(request):
  from admin.models import Country
  CountryFormSet = modelformset_factory(Country)
  context = {}
  if request.method == 'POST':
    formset = CountryFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  else:
    formset = CountryFormSet(queryset=Country.objects.all())
  context['formset'] = formset
  return render(request, 'admin/dashboard/formset.html', context)

def currency(request):
  from admin.models import Currency
  CurrencyFormSet = modelformset_factory(Currency)
  context = {}
  if request.method == 'POST':
    formset = CurrencyFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  else:
    formset = CurrencyFormSet(queryset=Currency.objects.all())
  context['formset'] = formset
  return render(request, 'admin/dashboard/formset.html', context)

def color(request):
  from admin.models import Color
  ColorFormSet = modelformset_factory(Color)
  context = {}
  if request.method == 'POST':
    formset = ColorFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  else:
    formset = ColorFormSet(queryset=Color.objects.all())
  context['formset'] = formset
  return render(request, 'admin/dashboard/formset.html', context)

def category(request):
  from admin.models import Category
  CategoryFormSet = modelformset_factory(Category)
  context = {}
  if request.method == 'POST':
    formset = CategoryFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  else:
    formset = CategoryFormSet(queryset=Category.objects.all())
  context['formset'] = formset
  return render(request, 'admin/dashboard/formset.html', context)

def rating_subject(request):
  from admin.models import RatingSubject
  RatingSubjectFormSet = modelformset_factory(RatingSubject)
  context = {}
  if request.method == 'POST':
    formset = RatingSubjectFormSet(request.POST)
    try:
      formset.save()
    except Exception as e:
      context['exception'] = e
  else:
    formset = RatingSubjectFormSet(queryset=RatingSubject.objects.all())
  context['formset'] = formset
  return render(request, 'admin/dashboard/formset.html', context)
