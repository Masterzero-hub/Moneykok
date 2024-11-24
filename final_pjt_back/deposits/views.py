from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
import requests
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta

from .models import DepositOptions, DepositProducts, Banks, DepositSpecialCondition, JoinedDeposits
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsSaveSerializer ,BanksSerializer, DepositProductsGETSerializer, DepositJoinSerializer, JoinedDepositSerializer

from dateutil.relativedelta import relativedelta
from django.db.models import Count
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from django.contrib.auth import get_user_model
User = get_user_model()

from datetime import date
from rest_framework.decorators import api_view, authentication_classes , permission_classes


# Create your views here.
##### 예금 상품 조회 #####
# 예금 상품 API를 통해 저장
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
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

# 예금상품 상세조회
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def deposit_detail(request, fin_prdt_cd):
    try:
        # 예금 상품 가져오기
        deposit = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
        
        # 직렬화 후 반환
        serializer = DepositProductsGETSerializer(deposit, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        # 기타 예외 처리
        return JsonResponse({'message': '예금 상품 정보를 가져오는 중 오류가 발생했습니다.', 'error': str(e)}, status=500)
    
from django.db.models import Q
from django.db.models import Max, Subquery, OuterRef

# 예금 상품 조회
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def deposits_list(request):
    data = request.GET  # GET 요청 데이터 가져오기
    filters = {key: (None if value in ['', [], '0'] else value) for key, value in data.items()}
    bank = filters.get('bank', None)  # 은행명 필터 (JSON 문자열 형태)
    conditions = filters.get('conditions', None)  # 우대조건 필터 (JSON 문자열 형태)
    join_term = filters.get('join_term', None)  # 가입 기간 필터
    amount = filters.get('amount', None)  # 가입금액 필터

    # QuerySet 생성
    products = DepositProducts.objects.all()

    # `save_trm=12` 조건의 최고 금리 가져오기
    options_with_save_trm_12 = DepositOptions.objects.filter(
        product=OuterRef('pk'), save_trm=12
    ).order_by('-intr_rate2')

    # fallback: 가장 마지막 `intr_rate2` 데이터 가져오기
    fallback_option = DepositOptions.objects.filter(
        product=OuterRef('pk')
    ).order_by('-id')

    # `save_trm=12`의 `intr_rate2`와 fallback 값을 결합하여 최종 금리 결정
    products = products.annotate(
        selected_intr_rate=Subquery(
            options_with_save_trm_12.values('intr_rate2')[:1]  # `save_trm=12` 금리
        )
    ).annotate(
        fallback_intr_rate=Subquery(
            fallback_option.values('intr_rate2')[:1]  # fallback 금리
        )
    ).annotate(
        final_intr_rate=Max('selected_intr_rate', 'fallback_intr_rate')  # 최종 금리
    )

    # 은행명 필터
    if bank:
        try:
            fin_co_no_list = json.loads(bank)  # JSON 문자열 -> Python 리스트로 변환
            products = products.filter(bank__fin_co_no__in=fin_co_no_list)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'fin_co_no는 유효한 JSON 배열이어야 합니다.'}, status=400)

    # 우대조건 카테고리 필터
    if conditions:
        try:
            category_list = json.loads(conditions)  # JSON 문자열 -> Python 리스트로 변환
            products = products.filter(
                Q(depositspecialcondition__category__in=category_list) |
                Q(depositspecialcondition__isnull=True)
            ).distinct()
        except json.JSONDecodeError:
            return JsonResponse({'message': 'special_condition_category는 유효한 JSON 배열이어야 합니다.'}, status=400)

    # 가입 기간 필터
    if join_term:
        try:
            join_term = int(join_term)  # 입력받은 기간을 정수로 변환
            products = products.filter(options__save_trm=join_term)
        except ValueError:
            return JsonResponse({'message': '잘못된 가입 기간 값입니다.'}, status=400)

    # 가입금액 필터
    if amount:
        try:
            amount = int(amount)  # 입력받은 금액을 정수로 변환
            products = products.filter(
                Q(deposit_min_amount__isnull=True, deposit_max_amount__isnull=True) |
                Q(deposit_min_amount__isnull=True, deposit_max_amount__gte=amount) |
                Q(deposit_max_amount__isnull=True, deposit_min_amount__lte=amount) |
                Q(deposit_min_amount__lte=amount, deposit_max_amount__gte=amount)
            )
        except ValueError:
            return JsonResponse({'message': '잘못된 가입금액 값입니다.'}, status=400)

    products = products.order_by('-final_intr_rate')

    # 조건에 맞는 데이터가 없을 경우 처리
    if not products.exists():
        return JsonResponse({'message': '조건에 맞는 데이터가 없습니다.', 'data': []}, status=404)

    # 직렬화 후 응답
    serializer = DepositProductsGETSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


import json
import re
from dotenv import load_dotenv
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import DepositProducts, DepositSpecialCondition
from groq import Groq

# .env 파일 로드
load_dotenv()

# Groq API 키 가져오기
GROQ_API_KEY = settings.GROQ_API_KEY
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")

# Groq 클라이언트 초기화
client = Groq(api_key=GROQ_API_KEY)

##### AI를 이용한 우대조건 카테고리화 ######
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

def parse_deposit_amount_ai(etc_note, ai_client):
    """
    AI를 사용해 가입금액 텍스트에서 최소 및 최대 금액을 분석합니다.
    """
    if not etc_note:
        return None, None
    # 프롬프트 작성
    prompt = f"""다음 텍스트에서 가입금액과 관련된 최소 및 최대 금액을 분석하세요. 텍스트에서 금액이 명시되어 있다면 '최소 금액'과 '최대 금액'을 정확히 추출하고, 금액 단위는 반드시 **만원 단위의 숫자**로 반환하세요.

    #### 규칙
    1. "최소", "최저", "이상", "초과" 키워드와 연결된 금액을 '최소 금액'으로 설정하세요.
    2. "최대", "최고", "이내", "이하", "미만" 키워드와 연결된 금액을 '최대 금액'으로 설정하세요.
    3. 금액 단위는 '원', '만원', '백만원', '천만원', '억원' 등을 포함할 수 있으며, 이를 **만원 단위**로 변환해야 합니다.
    4. 숫자만 명시된 경우 이를 만원 단위로 판단합니다.

    #### 텍스트 예시
    1. "1인당 최소 100만원 이상, 최대 10억원 이하"
    결과 :
    2. "가입금액: 1백만원 이상, 1억원 이내"
    3. "가입금액은 최소 50만원 이상입니다."

    #### 응답 형식
    결과를 JSON 형식으로 반환하세요:
    {{
        "min_amount": 최소 금액 (만원 단위),
        "max_amount": 최대 금액 (만원 단위)
    }}

    #### 텍스트:
    {etc_note}
    """

    try:
        response = ai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 금융 텍스트 분석 전문가입니다."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-70b-versatile",
            temperature=0,
            max_tokens=256,
        )

        if not response.choices or not response.choices[0].message:
            print("API 응답에 메시지가 없습니다.")
            return None, None

        assistant_message = response.choices[0].message.content.strip()
        try:
            amount_data = json.loads(assistant_message)
            return amount_data.get("min_amount"), amount_data.get("max_amount")
        except json.JSONDecodeError as e:
            print(f"JSON 디코딩 오류: {e}, 응답 내용: {assistant_message}")
            return None, None

    except Exception as e:
        print(f"예기치 못한 오류: {e}")
        return None, None

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def classify(request):
    """
    예금 상품의 우대조건 및 가입금액 데이터를 분석하고 저장.
    """
    products = DepositProducts.objects.all()

    # 우대조건 분석 및 저장
    for product in products:
        spcl_cnd = product.spcl_cnd.strip()
        if spcl_cnd and spcl_cnd not in ['우대조건 없음', '해당사항 없음', '없음']:
            parsed_conditions = parse_special_conditions(spcl_cnd)
            for condition in parsed_conditions:
                if not DepositSpecialCondition.objects.filter(
                    product=product,
                    **condition
                ).exists():
                    DepositSpecialCondition.objects.create(product=product, **condition)

        # 가입금액 분석 및 저장
        etc_note = product.etc_note.strip()
        if etc_note:
            min_amount, max_amount = parse_deposit_amount_ai(etc_note, client)
            print(f"가입금액 파싱 결과: {etc_note} -> 최소: {min_amount}, 최대: {max_amount}")  # 로그 추가
            if min_amount is not None and max_amount is not None:
                product.deposit_min_amount = min_amount
                product.deposit_max_amount = max_amount
                product.save()
            else:
                print(f"가입금액 파싱 실패: {etc_note}")

    return JsonResponse({'message': '우대조건 및 가입금액 정보 저장 완료'})




##### 상품 가입하기 #####
@api_view(['POST'])
def deposit_join(request, fin_prdt_cd):
    try:
        # 로그인된 사용자
        user = request.user

        # 예금 상품 정보 가져오기
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        except DepositProducts.DoesNotExist:
            return Response({'error': '해당 상품이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 요청 데이터 가져오기
        save_trm = request.data.get('save_trm')  # 가입 기간 (개월)
        save_amount = request.data.get('save_amount')  # 가입 금액 (만 원 단위)
        final_intr_rate = request.data.get('final_intr_rate')  # 사용자 요청 금리

        if not save_trm or not save_amount or final_intr_rate is None:
            return Response({'error': '가입 기간(save_trm), 금액(save_amount), 금리(final_intr_rate)를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 입력 값 검증
        try:
            save_trm = int(save_trm)
            save_amount = int(save_amount) * 10000
            final_intr_rate = float(final_intr_rate)
        except ValueError:
            return Response({'error': '입력 값은 숫자 형식이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 최소 및 최대 가입 금액 확인
        deposit_min_amount = product.deposit_min_amount or 0
        deposit_max_amount = product.deposit_max_amount

        if save_amount < deposit_min_amount:
            return Response({'error': f'가입 금액은 최소 {deposit_min_amount}원 이상이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if deposit_max_amount and save_amount > deposit_max_amount:
            return Response({'error': f'가입 금액은 최대 {deposit_max_amount}원을 초과할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 적합한 옵션 필터링 (기간만 확인)
        valid_options = [
            option for option in product.options.all()
            if option.save_trm == save_trm
        ]

        if not valid_options:
            return Response({'error': f'{save_trm}개월에 해당하는 옵션이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 만기일 계산
        try:
            expired_date = now().date() + relativedelta(months=save_trm)
        except Exception as e:
            return Response({'error': f'만기일 계산 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 데이터 저장
        joined_deposit = JoinedDeposits.objects.create(
            user=user,
            product=product,
            save_trm=save_trm,
            save_amount=save_amount,
            expired_date=expired_date,
            final_intr_rate=final_intr_rate
        )

        # 결과 반환
        serializer = DepositJoinSerializer(joined_deposit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': f'서버 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({'error': f'서버 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 가입한 상품 목록 보여주기
@api_view(["GET"])
def joined_products(request):
    try:
        user = request.user
        # 특정 사용자의 가입 데이터를 가져옴
        joined_products = JoinedDeposits.objects.filter(user=user)

        if not joined_products.exists():
            return Response({"message": "No subscriptions found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # 만기일 기준으로 정렬
        joined_products = sorted(joined_products, key=lambda x: x.expired_date)

        # 직렬화
        serializer = JoinedDepositSerializer(joined_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'서버 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def recommend_products(request):
    user = request.user

    # Step 0: 현재 로그인된 사용자 정보 가져오기
    income = user.income
    birth_year = user.birthdate.year
    gender = user.gender

    # Step 1: 필터링된 상품 가져오기
    filtered_products = DepositProducts.objects.all()  # 기본적으로 모든 상품
    # 추가적인 필터 조건이 있다면 적용 가능:
    # filtered_products = filtered_products.filter(min_income__lte=income)

    # Step 2: 유사한 사용자 찾기
    user_data = np.array([[income, birth_year, 1 if gender == '남성' else 0]])
    all_users = User.objects.exclude(id=user.id)

    similar_users = []
    for other_user in all_users:
        other_data = np.array([[other_user.income, other_user.birthdate.year, 1 if other_user.gender == '남성' else 0]])
        similarity = cosine_similarity(user_data, other_data)
        similar_users.append((other_user, similarity[0][0]))

    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:10]

    # Step 3: 유사 사용자가 가입한 상품 가져오기
    similar_user_ids = [u[0].id for u in similar_users]
    joined_deposits = JoinedDeposits.objects.filter(user_id__in=similar_user_ids)

    # 상품별 추천 점수 계산
    product_scores = (
        joined_deposits
        .values('product_id')
        .annotate(score=Count('product_id'))
        .order_by('-score')
    )

    # 상위 3개 상품 추천
    recommended_product_ids = [p['product_id'] for p in product_scores[:3]]
    recommended_products = DepositProducts.objects.filter(id__in=recommended_product_ids)

    serializer = DepositProductsGETSerializer(recommended_products, many=True)
    return Response({'recommended_products': serializer.data})
