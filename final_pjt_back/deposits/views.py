from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
import requests
from rest_framework.response import Response



from .models import DepositOptions, DepositProducts, Banks, DepositSpecialCondition
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


import os
from dotenv import load_dotenv
from django.http import JsonResponse
from .models import DepositProducts, DepositSpecialCondition
from django.conf import settings
from groq import Groq

# .env 파일 로드
load_dotenv()

# Groq API 키 가져오기
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")

# Groq 클라이언트 초기화
client = Groq(api_key=api_key)

def save_special_conditions(request):
    products = DepositProducts.objects.all()
    for product in products:
        spcl_cnd = product.spcl_cnd.strip()
        if spcl_cnd and spcl_cnd != '해당사항 없음':
            # AI 서비스에 요청하여 우대조건 정보를 파싱합니다.
            parsed_conditions = parse_special_conditions(spcl_cnd)
            for condition in parsed_conditions:
                condition_name = condition.get('condition_name')
                prime_rate = condition.get('prime_rate')
                fin_prdt_cd = product.fin_prdt_cd

                # 이미 동일한 우대조건이 존재하는지 확인합니다.
                if DepositSpecialCondition.objects.filter(
                    product=product,
                    condition_name=condition_name,
                    prime_rate=prime_rate
                ).exists():
                    continue

                # 우대조건 정보를 저장합니다.
                DepositSpecialCondition.objects.create(
                    product=product,
                    fin_prdt_cd=fin_prdt_cd,
                    condition_name=condition_name,
                    prime_rate=prime_rate
                )
    return JsonResponse({'message': '우대조건 정보 저장 완료'})

def parse_special_conditions(spcl_cnd_text):
    # Groq API를 호출하여 spcl_cnd_text를 파싱하는 로직을 구현합니다.

    prompt = f"""다음 텍스트에서 우대조건과 우대금리를 추출하세요:

우대조건 텍스트:
{spcl_cnd_text}

출력 형식:
[
    {{
        "condition_name": "우대조건 이름",
        "prime_rate": 우대금리 (숫자형, % 단위)
    }},
    ...
]
"""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 우대조건 정보를 추출하는 전문가입니다."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-70b-versatile",
            temperature=0,
            max_tokens=4096,
            top_p=1,
            stream=False,
            stop=None,
        )
        assistant_message = response.choices[0].message.content.strip()
        # 응답된 텍스트를 JSON으로 변환합니다.
        import json
        parsed_conditions = json.loads(assistant_message)
        return parsed_conditions

    except Exception as e:
        print(f"우대조건 파싱 오류: {e}")
        return []

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