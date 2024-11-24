import os
import django

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

 
import json
import re
import time
from django.conf import settings
from deposits.models import DepositOptions, DepositProducts, Banks
from deposits.serializers import (
    BanksSerializer,
    DepositOptionsSerializer,
    DepositProductsSaveSerializer,
)
from savings.models import SavingsOptions, SavingsProducts, Banks
from savings.serializers import (
    SavingsOptionsSerializer,
    SavingsProductsSaveSerializer,
)

import requests

def deposits_products():
    """
    금융감독원 API 데이터를 가져와 저장하고 AI 분석을 수행합니다.
    """
    URL = settings.DEPOSIT_URL + 'depositProductsSearch.json'
    params ={
        'auth': settings.API_KEY,
        'topFinGrpNo':'020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=params).json()
    for baselist in response.get('result')['baseList']:
            fin_prdt_cd = baselist.get('fin_prdt_cd')
            fin_co_no = baselist.get('fin_co_no')
            kor_co_nm = baselist.get('kor_co_nm')
            fin_prdt_nm = baselist.get('fin_prdt_nm')
            etc_note = baselist.get('etc_note')
            join_deny = baselist.get('join_deny')
            join_member = baselist.get('join_member')
            join_way = baselist.get('join_way')
            spcl_cnd = baselist.get('spcl_cnd')
            
            try:
                bank = Banks.objects.get(fin_co_no=fin_co_no, kor_co_nm=kor_co_nm)
            except Banks.DoesNotExist:
                save_data_B = {
                    'fin_co_no': fin_co_no,
                    'kor_co_nm': kor_co_nm,
                }
                serializerBanks = BanksSerializer(data=save_data_B)
                if serializerBanks.is_valid(raise_exception=True):
                    bank = serializerBanks.save()

            if not DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                save_data_P = {
                    'fin_prdt_cd': fin_prdt_cd,
                    'fin_prdt_nm': fin_prdt_nm,
                    'etc_note': etc_note,
                    'join_deny': join_deny,
                    'join_member': join_member,
                    'join_way': join_way,
                    'spcl_cnd': spcl_cnd,
                }
                serializerProducts = DepositProductsSaveSerializer(data=save_data_P)
                if serializerProducts.is_valid(raise_exception=True):
                    serializerProducts.save(bank=bank)


    for optionlist in response.get('result')['optionList']:
        fin_prdt_cd = optionlist.get('fin_prdt_cd')
        intr_rate_type_nm = optionlist.get('intr_rate_type_nm')
        intr_rate = optionlist.get('intr_rate') 
        intr_rate2 = optionlist.get('intr_rate2')
        save_trm = optionlist.get('save_trm')

        if not intr_rate:
            try : 
                if DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)[intr_rate]:
                    intr_rate = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)['intr_rate']
            except:
                continue
        if not intr_rate2:
            try : 
                if DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)[intr_rate2]:
                    intr_rate2 = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)['intr_rate']
            except:
                continue

        products = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd)
        for product in products:
            # 중복 데이터 확인
            if DepositOptions.objects.filter(
                product=product,
                intr_rate_type_nm=intr_rate_type_nm,
                intr_rate=intr_rate,
                intr_rate2=intr_rate2,
                save_trm=save_trm
            ).exists():
                continue

            # DepositOptions 저장
            save_data_O = {
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
            }
            serializerOptions = DepositOptionsSerializer(data=save_data_O)
            if serializerOptions.is_valid(raise_exception=True):
                serializerOptions.save(product=product)

    print("예금 상품 저장")

def savings_products():
    """
    금융감독원 API 데이터를 가져와 저장하고 AI 분석을 수행합니다.
    """
    URL = settings.PRODUCTS_URL + 'savingProductsSearch.json'
    params = {'auth': settings.API_KEY, 'topFinGrpNo': '020000', 'pageNo': 1}
    response = requests.get(URL, params=params).json()

    # Bank 저장
    for baselist in response.get('result')['baseList']:
        fin_co_no = baselist.get('fin_co_no')
        kor_co_nm = baselist.get('kor_co_nm')

        bank, _ = Banks.objects.get_or_create(fin_co_no=fin_co_no, kor_co_nm=kor_co_nm)

        # DepositProduct 저장
        fin_prdt_cd = baselist.get('fin_prdt_cd')
        if not SavingsProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            product_data = {
                'fin_prdt_cd': fin_prdt_cd,
                'fin_prdt_nm': baselist.get('fin_prdt_nm'),
                'etc_note': baselist.get('etc_note'),
                'join_deny': baselist.get('join_deny'),
                'join_member': baselist.get('join_member'),
                'join_way': baselist.get('join_way'),
                'spcl_cnd': baselist.get('spcl_cnd'),
            }

            serializer = SavingsProductsSaveSerializer(data=product_data)
            if serializer.is_valid(raise_exception=True):
                product = serializer.save(bank=bank)

    # DepositOptions 저장
    for optionlist in response.get('result')['optionList']:
        fin_prdt_cd = optionlist.get('fin_prdt_cd')
        intr_rate_type_nm = optionlist.get('intr_rate_type_nm')
        intr_rate = optionlist.get('intr_rate') 
        intr_rate2 = optionlist.get('intr_rate2')
        save_trm = optionlist.get('save_trm')

        if not intr_rate:
            try : 
                if SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)[intr_rate]:
                    intr_rate = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)['intr_rate']
            except:
                continue
        if not intr_rate2:
            try : 
                if SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)[intr_rate2]:
                    intr_rate2 = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)['intr_rate']
            except:
                continue

        products = SavingsProducts.objects.filter(fin_prdt_cd=fin_prdt_cd)
        for product in products:
            # 중복 데이터 확인
            if SavingsOptions.objects.filter(
                product=product,
                intr_rate_type_nm=intr_rate_type_nm,
                intr_rate=intr_rate,
                intr_rate2=intr_rate2,
                save_trm=save_trm
            ).exists():
                continue

            # DepositOptions 저장
            save_data_O = {
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
            }
            serializerOptions = SavingsOptionsSerializer(data=save_data_O)
            if serializerOptions.is_valid(raise_exception=True):
                serializerOptions.save(product=product)

    print("적금 상품 저장")

deposits_products()
savings_products()