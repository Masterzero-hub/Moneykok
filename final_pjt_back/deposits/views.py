from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
import requests


from .models import DepositOptions, DepositProducts
from .serializers import DepositOptionsSerializer, DepositProductsSerializer


# Create your views here.
def save_products(request):
    URL = settings.DEPOSIT_URL +'depositProductsSearch.json'
    params ={
        'auth': settings.API_KEY,
        'topFinGrpNo':'020000',
        'pageNo': 1,
    }
