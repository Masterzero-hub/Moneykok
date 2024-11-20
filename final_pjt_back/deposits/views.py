from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
import requests
from rest_framework.response import Response



from .models import DepositOptions, DepositProducts, Banks
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, BanksSerializer

# Create your views here.
@api_view(['GET'])
def save_products(request):
    URL = settings.DEPOSIT_URL +'depositProductsSearch.json'
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
            
            if not Banks.objects.filter(fin_co_no=fin_co_no, kor_co_nm=kor_co_nm).exists():
                save_data_B = {
                    'fin_co_no': fin_co_no,
                    'kor_co_nm': kor_co_nm,
                }

                serializerBanks = BanksSerializer(data=save_data_B) 
                if serializerBanks.is_valid(raise_exception=True):
                    serializerBanks.save()

            if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd,fin_co_no=fin_co_no,
                                            fin_prdt_nm=fin_prdt_nm,etc_note=etc_note,
                                            join_deny= join_deny,join_member= join_member,
                                            join_way= join_way,spcl_cnd= spcl_cnd).exists():
                continue    

            save_data_P ={
                'fin_prdt_cd':fin_prdt_cd,
                'fin_co_no':fin_co_no,
                'fin_prdt_nm':fin_prdt_nm,
                'etc_note':etc_note,
                'join_deny':join_deny,
                'join_member':join_member,
                'join_way':join_way,
                'spcl_cnd':spcl_cnd,
            }

            bank = Banks.objects.get(fin_co_no=fin_co_no)
            serializerProducts = DepositProductsSerializer(data=save_data_P) 
            if serializerProducts.is_valid(raise_exception=True):
                serializerProducts.save(bank= bank)

    for optionlist in response.get('result')['optionList']:
        fin_prdt_cd = optionlist.get('fin_prdt_cd')
        intr_rate_type_nm = optionlist.get('intr_rate_type_nm')
        intr_rate = optionlist.get('intr_rate') 
        intr_rate2 = optionlist.get('intr_rate2')
        save_trm = optionlist.get('save_trm')

        intr_rate = intr_rate if intr_rate else -1
        intr_rate2 = intr_rate2 if intr_rate2 else -1
        

        if DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd,
                                        intr_rate_type_nm=intr_rate_type_nm,
                                        intr_rate=intr_rate,
                                        intr_rate2=intr_rate2,
                                        save_trm= save_trm).exists():
            continue 

        save_data_O ={
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm,
        }

        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializerOptions = DepositOptionsSerializer(data=save_data_O) 
        if serializerOptions.is_valid(raise_exception=True):
            serializerOptions.save(product=product)

    return JsonResponse({'message':'예금 상품 저장'})

@api_view(['GET'])
def products_all_list(request):
    if request.method == "GET":
        products = DepositProducts.objects.all()
        serializers = DepositProductsSerializer(products,many=True)
        return Response(serializers.data)

@api_view(['GET'])
def products_query_list(request):
    fin_prdt_cd = request.GET.get('fin_prdt_cd')
    fin_co_no = request.GET.get('fin_co_no')
    fin_prdt_nm = request.GET.get('fin_prdt_nm')
    join_deny = request.GET.get('join_deny')
    # 필요에 따라 추가적인 필터링 조건을 가져옵니다.

    filters = {}
    if fin_prdt_cd:
        filters['fin_prdt_cd'] = fin_prdt_cd
    if fin_co_no:
        filters['fin_co_no'] = fin_co_no
    if fin_prdt_nm:
        filters['fin_prdt_nm__icontains'] = fin_prdt_nm
    if join_deny:
        filters['join_deny'] = join_deny

    products = DepositProducts.objects.filter(**filters)
    serializer = DepositProductsSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)