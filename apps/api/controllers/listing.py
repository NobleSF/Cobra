from rest_framework import serializers
from apps.api.models.listing import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'name', 'store',)

#http://www.django-rest-framework.org/tutorial/1-serialization



#from django.http import HttpResponse
#from django.shortcuts import render, get_object_or_404
#from apps.admin.utils.exception_handling import ExceptionHandler
#from django.views.decorators.cache import cache_page
#import json
#
#def product(request): pass
#"""
#use django-rest to serve public product data
#similar to the product_data feed already in use.
#
#
#
#"""
