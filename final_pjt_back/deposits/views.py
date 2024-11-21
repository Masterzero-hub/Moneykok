from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
import requests
from rest_framework.response import Response



from .models import DepositOptions, DepositProducts, Banks, DepositSpecialCondition
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsSaveSerializer ,BanksSerializer, DepositProductsGETSerializer

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

    return JsonResponse({'message': '예금 상품 및 옵션 저장 완료'})


# @api_view(['GET'])
# def products_all_list(request):
#     if request.method == "GET":
#         # prefetch_related를 사용해 옵션 데이터 로드 최적화
#         products = DepositProducts.objects.prefetch_related('options', 'bank').all()
#         serializers = DepositProductsGETSerializer(products, many=True)
#         return Response(serializers.data)

from django.db.models import Q

@api_view(['GET'])
def deposits_list(request):
    kor_co_nm = request.GET.get('kor_co_nm')  # 은행명 필터
    special_condition_category = request.GET.get('special_condition_category')  # 우대조건 카테고리 필터
    join_term = request.GET.get('join_term')  # 가입 기간 필터 (단위: 개월)
    deposit_amount = request.GET.get('deposit_amount')  # 가입금액 필터

    # QuerySet 생성 (prefetch_related로 최적화)
    products = DepositProducts.objects.prefetch_related('options', 'bank').all()

    # 은행명 필터
    if kor_co_nm:
        products = products.filter(bank__kor_co_nm__icontains=kor_co_nm)

    # 우대조건 카테고리 필터
    if special_condition_category:
        # 쉼표로 분리된 값을 리스트로 변환
        categories = [category.strip() for category in special_condition_category.split(',')]
        products = products.filter(
            Q(depositspecialcondition__category__in=categories) |
            Q(depositspecialcondition__isnull=True)
        ).distinct()

    # 가입 기간 필터
    if join_term:
        try:
            join_term = int(join_term)  # 입력받은 기간을 정수로 변환

            # 옵션에서 입력된 가입 기간과 정확히 매칭되는 조건만 필터링
            filtered_products = []
            for product in products:
                # 해당 상품의 옵션 중 save_trm이 join_term과 일치하는 옵션만 선택
                options = product.options.filter(save_trm=join_term)
                if options.exists():  # 조건에 맞는 옵션이 있는 경우에만 상품 포함
                    product.best_option = options.first()  # 일치하는 첫 번째 옵션 추가
                    filtered_products.append(product)

            products = filtered_products  # 필터링된 상품 리스트로 교체
        except ValueError:
            return JsonResponse({'message': '잘못된 가입 기간 값입니다.'}, status=400)

    # 가입금액 필터
    if deposit_amount:
        try:
            deposit_amount = int(deposit_amount)  # 입력받은 금액을 정수로 변환
            
            # DepositProducts에서 직접 필터링
            products = products.filter(
                Q(deposit_min_amount__isnull=True, deposit_max_amount__isnull=True) |  # 두 필드가 NULL인 경우
                Q(deposit_min_amount__isnull=True, deposit_max_amount__gte=deposit_amount) |  # 최소 금액만 NULL
                Q(deposit_max_amount__isnull=True, deposit_min_amount__lte=deposit_amount) |  # 최대 금액만 NULL
                Q(deposit_min_amount__lte=deposit_amount, deposit_max_amount__gte=deposit_amount)  # 둘 다 값이 있는 경우
            )
        except ValueError:
            return JsonResponse({'message': '잘못된 가입금액 값입니다.'}, status=400)

    # 조건에 맞는 데이터가 없을 경우 처리
    if not products:
        return JsonResponse({'message': '조건에 맞는 데이터가 없습니다.', 'data': []}, status=404)

    # 직렬화 후 응답
    serializer = DepositProductsGETSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

from dotenv import load_dotenv
from django.http import JsonResponse
from .models import DepositProducts, DepositSpecialCondition
from django.conf import settings
from groq import Groq
import json
import re

# .env 파일 로드
load_dotenv()

# Groq API 키 가져오기
GROQ_API_KEY = settings.GROQ_API_KEY
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")

# Groq 클라이언트 초기화
client = Groq(api_key=GROQ_API_KEY)

def parse_special_conditions(spcl_cnd_text):
    """
    AI를 사용해 spcl_cnd_text에서 우대조건, 금리, 세부내용을 추출합니다.
    """
    """
    Groq API를 사용해 spcl_cnd_text에서 우대조건, 금리, 세부내용을 추출합니다.
    """
    prompt = f"""다음 텍스트에서 우대조건, 세부내용, 금리를 정확히 추출하고, 각 우대조건을 아래의 카테고리 중 하나로 분류하세요. 카테고리 분류와 추출은 텍스트의 모든 세부 조건을 포함하며, 반드시 명시된 형식으로만 응답해야 합니다.

    #### 카테고리
    각 우대조건을 아래 6가지 카테고리 중 하나로 분류합니다. 
    - 거래 연동: 급여이체, 자동이체, 계좌 연결, 이체와 같이 거래 내역, 계좌 간 연동과 관련된 조건.
    - 사용 실적: 카드 결제, 사용 금액, 소비와 같이 고객의 금융 활동, 소비 기록 등 실적 기반 조건.
    - 신규 가입: 신규 고객, 첫 거래, 가입 후 등 신규 가입 관련 조건.
    - 비대면/모바일 뱅킹: 모바일, 비대면, 앱 가입 등 비대면 채널 이용과 관련된 조건.
    - 마케팅 및 기타 동의: 마케팅 동의, 개인정보 활용, 이벤트 동의 등 고객 동의와 관련된 조건.
    - 기타: 위 조건에 속하지 않는 특별 조건 또는 기타 명시되지 않은 사항.

    #### 텍스트:
    {spcl_cnd_text}

    #### 응답 형식
    [
        {{
            "category": "카테고리 이름 (거래 연동, 사용 실적, 신규 가입, 비대면/모바일 뱅킹, 마케팅 및 기타 동의, 기타 중 하나)",
            "condition_title": "우대조건 요약",
            "condition_content": "우대조건 상세 설명",
            "prime_rate": 숫자형 금리 (예: 0.1)
        }},
        ...
    ]
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 우대조건 정보를 분석하는 전문가입니다."},
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

        # JSON 데이터만 추출
        json_data_match = re.search(r'\[.*\]', assistant_message, re.DOTALL)
        if json_data_match:
            json_data = json_data_match.group()
            parsed_conditions = json.loads(json_data)
            return parsed_conditions
        else:
            print("JSON 데이터를 찾을 수 없습니다.")
            return []
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")
        return []
    except Exception as e:
        print(f"예기치 못한 오류: {e}")
        return []

def classify(request):
    """
    모든 예금 상품의 우대조건 데이터를 분석하고 저장합니다.
    """
    products = DepositProducts.objects.all()
    for product in products:
        spcl_cnd = product.spcl_cnd.strip()
        if spcl_cnd and spcl_cnd not in ['우대조건 없음', '해당사항 없음', '없음']:

            parsed_conditions = parse_special_conditions(spcl_cnd)
            for condition in parsed_conditions:
                category = condition.get('category')
                condition_title = condition.get('condition_title')
                condition_content = condition.get('condition_content')
                prime_rate = condition.get('prime_rate')

                # 이미 동일한 우대조건이 존재하는지 확인
                if DepositSpecialCondition.objects.filter(
                    product=product,
                    category=category,
                    condition_title=condition_title,
                    condition_content=condition_content,
                    prime_rate=prime_rate,
                ).exists():
                    continue

                # 우대조건 정보를 저장
                DepositSpecialCondition.objects.create(
                    product=product,
                    category=category,
                    condition_title=condition_title,
                    condition_content=condition_content,
                    prime_rate=prime_rate,
                )

    """
    DepositProducts의 가입금액 데이터를 분석하여 (만원) 단위로 저장합니다.
    """
    products = DepositProducts.objects.all()
    for product in products:
        etc_note = product.etc_note.strip()
        if etc_note:
            # 가입금액 분석
            min_amount, max_amount = parse_deposit_amount(etc_note)

            # 분석된 데이터를 모델 필드에 저장
            product.deposit_min_amount = min_amount
            product.deposit_max_amount = max_amount
            product.save()

    return JsonResponse({'message': '우대조건 및 가입금액 정보 저장 완료'})

def categorize_condition(condition_name):
    """
    우대조건 이름을 기반으로 6가지 카테고리 중 하나로 분류합니다.
    """
    category_keywords = {
        "거래 연동": ["거래", "연동", "계좌 연결", "자동이체", "이체", "급여"],
        "사용 실적": ["사용", "실적", "카드", "결제", "이용 금액", "소비"],
        "신규 가입": ["신규", "가입", "처음", "가입 후", "가입자"],
        "비대면/모바일 뱅킹": ["비대면", "모바일", "뱅킹", "앱", "스마트폰", "온라인"],
        "마케팅 및 기타 동의": ["마케팅", "동의", "개인정보", "프로모션", "광고"],
        "기타": ["기타", "별도", "추가", "특별", "조건 없음"],
    }

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in condition_name:
                return category
    return "기타"  # 기본값으로 기타 반환

def parse_deposit_amount(etc_note):
    """
    가입금액 텍스트를 분석하여 최소 및 최대 금액을 숫자(만원 단위)로 반환합니다.
    """
    if not etc_note:
        return None, None

    # 금액을 숫자(만원)로 변환
    def convert_to_number(text):
        text = text.replace(',', '').replace(' ', '')  # 쉼표와 공백 제거
        if '억원' in text:
            return int(float(text.replace('억원', '')) * 10000)  # 1억 = 10,000만원
        elif '천만원' in text:
            return int(float(text.replace('천만원', '')) * 1000)  # 1천만 = 1,000만원
        elif '백만원' in text:
            return int(float(text.replace('백만원', '')) * 100)  # 1백만 = 100만원
        elif '만원' in text:
            return int(text.replace('만원', ''))  # 1만원 단위 그대로
        else:
            # 숫자만 주어진 경우 (만원 단위로 판단)
            return int(re.sub(r'\D', '', text))  # 숫자 외 제거 후 숫자로 변환

    # 최소/최대 금액 초기화
    min_amount, max_amount = None, None

    # "이상", "초과" 조건에서 최소 금액 파싱
    if '이상' in etc_note or '초과' in etc_note:
        match = re.search(r'\d+[백|천|억]?만원?', etc_note)
        if match:
            min_amount = convert_to_number(match.group())

    # "이하", "미만" 조건에서 최대 금액 파싱
    if '이하' in etc_note or '미만' in etc_note:
        match = re.search(r'\d+[백|천|억]?만원?', etc_note)
        if match:
            max_amount = convert_to_number(match.group())

    return min_amount, max_amount