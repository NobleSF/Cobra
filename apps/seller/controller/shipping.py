from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson
from math import ceil as roundUp

def calculateShippingCost(weight, shipping_option):
  shipping_cost = 9999
  rates = {}

  if (shipping_option.country.code == 'MA') and (shipping_option.name == 'Envelope'):
    rates = {
      '20': '14',
      '40': '29.5',
      '60': '35.7',
      '80': '42',
      '100': '48.2',
      '150': '80.9',
      '200': '93.3',
      '250': '112',
      '300': '150',
      '350': '168.7',
      '400': '181.1',
      '450': '199.8',
      '500': '212.2',
      '750': '331.1',
      '1000': '405.9',
      '2000': '777.5'
    }

  elif (shipping_option.country.code == 'MA') and (shipping_option.name == 'Package'):
    rates = {
      '1000': '186',
      '2000': '265',
      '3000': '344',
      '4000': '422',
      '5000': '502',
      '6000': '582',
      '7000': '662',
      '8000': '743',
      '9000': '823',
      '10000': '904',
      '11000': '985',
      '12000': '1067',
      '13000': '1148'
    }

  for weight_limit, cost in rates.iteritems():
    if int(weight) <= int(weight_limit) and float(cost) < shipping_cost:
      shipping_cost = float(cost)

  return int(roundUp(shipping_cost))
