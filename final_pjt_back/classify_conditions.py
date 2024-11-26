# -*- coding: utf-8 -*-
import os
import django

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

import json
import re
from django.conf import settings
from groq import Groq

from deposits.models import DepositProducts, DepositSpecialCondition
from savings.models import SavingsProducts, SavingsSpecialCondition

# Groq API 키 가져오기

##### AI를 이용한 우대조건 카테고리화 ######
def parse_special_conditions(spcl_cnd_text, API_KEY):
    GROQ_API_KEY = API_KEY
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")

    # Groq 클라이언트 초기화
    client = Groq(api_key=GROQ_API_KEY)
    """
    AI를 사용해 spcl_cnd_text에서 우대조건, 금리, 세부내용을 추출합니다.
    """
    prompt = f"""
    다음 텍스트는 특정 금융 상품의 우대조건을 포함하고 있습니다. 아래의 규칙에 따라 각 조건을 분석하고, 반드시 명시된 형식으로 응답하세요. 

    #### 처리 방법
    1. **조건 번호와 상세 설명 추출**:
    - 각 조건은 번호(1., 2., 3. 등)로 시작합니다.
    - 번호 뒤에 나오는 모든 내용을 우대조건의 상세 설명으로 간주하며, 이를 **condition_content** 필드에 그대로 포함합니다. 텍스트의 모든 세부 내용을 누락 없이 입력하세요.

    2. **금리 추출**:
    - 금리는 '%p' 또는 "X.XX%" 형식으로 표시됩니다. 이를 숫자형 금리(예: 0.1)로 변환하여 **prime_rate** 필드에 저장합니다. 
    - 금리가 없는 조건은 **prime_rate** 필드를 포함하지 않습니다.

    3. **카테고리 분류**:
    - 각 우대조건을 아래 6가지 카테고리 중 하나로 분류합니다:
        - 거래 연동: 급여이체, 자동이체, 계좌 연결, 이체 등 거래 내역이나 계좌 간 연동과 관련된 조건.
        - 사용 실적: 카드 결제, 사용 금액, 소비 등 고객의 금융 활동 및 소비 기록 기반 조건.
        - 신규 가입: 신규 고객, 첫 거래, 가입 후 등 신규 가입과 관련된 조건.
        - 비대면/모바일 뱅킹: 모바일, 비대면, 앱 가입 등 비대면 채널 이용과 관련된 조건.
        - 마케팅 및 기타 동의: 마케팅 동의, 개인정보 활용, 이벤트 동의 등 고객 동의와 관련된 조건.
        - 기타: 위 조건에 속하지 않는 특별 조건 또는 기타 명시되지 않은 사항.


    #### 텍스트
    {spcl_cnd_text}

    #### 응답 형식
    [
        {{
            "category": "카테고리 이름 (거래 연동, 사용 실적, 신규 가입, 비대면/모바일 뱅킹, 마케팅 및 기타 동의, 기타 중 하나)",
            "condition_content": "우대조건 상세 설명 (예: '상품 가입 전 최근 1개월 이내 인터넷/폰/모바일앱뱅킹 가입')",
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
            model="llama-3.2-90b-text-preview",
            temperature=0.2,
            max_tokens=4096,
            top_p=0.9,
        )
        assistant_message = response.choices[0].message.content.strip()

        # JSON 데이터만 추출
        json_data_match = re.search(r'\[.*\]', assistant_message, re.DOTALL)
        if json_data_match:
            parsed_conditions = json.loads(json_data_match.group())

            # 모델에 정의되지 않은 필드 제거 및 prime_rate 검증
            valid_conditions = [
                {key: value for key, value in condition.items()
                if key in ['category', 'condition_title', 'condition_content', 'prime_rate']}
                for condition in parsed_conditions
                if isinstance(condition.get("prime_rate"), (int, float))  # prime_rate가 숫자인 경우만 포함
            ]
            return valid_conditions
        else:
            print("JSON 데이터를 찾을 수 없습니다.")
            return []
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")
        return []
    except Exception as e:
        print(f"예기치 못한 오류: {e}")
        return []


def analyze_conditions(product_type, model, API_KEY):
    """
    주어진 상품 목록의 우대조건 데이터를 분석.
    """
    if product_type == "deposits":
        products = DepositProducts.objects.all()
    else:
        products = SavingsProducts.objects.all()
    
    for product in products:
        if not product.processed_spcl_cnd:
            continue
        spcl_cnd = product.processed_spcl_cnd.strip()
        
        parsed_conditions = parse_special_conditions(spcl_cnd, API_KEY)
        for condition in parsed_conditions:
            # 공통 저장 로직
            if condition.get('prime_rate') is None:
                print(f"prime_rate가 없어 저장하지 않음: {condition}")
                continue
            

            # 조건이 이미 존재하는지 확인하고 저장
            if not model.objects.filter(product=product, **condition).exists():
                try:
                    model.objects.create(product=product, **condition)
                except Exception as e:
                    print(f"조건 저장 중 오류 발생: {e} - {condition}")
    print(f"{product_type.capitalize()} 데이터 저장 완료")


# 실행 로직
# analyze_conditions("deposits", DepositSpecialCondition, settings.GROQ_API_KEY1)

# analyze_conditions("savings", SavingsSpecialCondition, settings.GROQ_API_KEY2)


def preprocess_deposit_amounts_with_ai(products, API_KEY):


    # Groq API 키 가져오기
    api_key = API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")

    # Groq 클라이언트 초기화
    client = Groq(api_key=api_key)
    """
    AI를 사용하여 etc_note 데이터를 전처리합니다.
    """

    for product in products:
        etc_note_text = product.etc_note.strip() if product.etc_note else None

        # etc_note가 비어있는 경우 처리
        if not etc_note_text:
            print(f"Product ID {product.id}: etc_note가 비어 있습니다.")
            product.savings_min_amount = None
            product.savings_max_amount = None
            product.save()
            continue

        # AI로 etc_note 파싱
        prompt = f"""다음 텍스트에서 가입금액과 관련된 최소 및 최대 금액을 분석하세요. 
        텍스트에서 금액이 명시되어 있다면 '최소 금액'과 '최대 금액'을 정확히 추출하고, 금액 단위는 반드시 **만원 단위의 숫자**로 반환하세요.
        
        #### 규칙:
        1. "최소", "최저", "이상", "초과" 키워드와 연결된 금액을 '최소 금액'으로 설정하세요.
        2. "최대", "최고", "이내", "이하", "미만" 키워드와 연결된 금액을 '최대 금액'으로 설정하세요.
        3. 금액 단위는 '원', '만원', '백만원', '천만원', '억원' 등을 포함할 수 있으며, 이를 **만원 단위**로 변환해야 합니다.
        4. 숫자만 명시된 경우 이를 만원 단위로 판단합니다.
        5. 가입금액 한도에 대해 나타내고 있는 정보가 없다면, NULL을 허용합니다.
        #### 텍스트:
        {etc_note_text}

        #### 응답 형식:
        {{
            "min_amount": 최소 금액 (만원 단위),
            "max_amount": 최대 금액 (만원 단위)
        }} 
        설명 문구는 포함하지 말고 출력 형식만 반환하세요.
        """

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "당신은 금융 데이터 분석 전문가입니다."},
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.2-11b-text-preview",
                temperature=0.2,
                max_tokens=4096,
                top_p=0.9,
            )
            assistant_message = response.choices[0].message.content.strip()

            # JSON 결과 파싱
            amount_data = json.loads(assistant_message)
            # 결과를 모델에 저장
            product.savings_min_amount = amount_data.get("min_amount")
            product.savings_max_amount = amount_data.get("max_amount")
            product.save()

            print(f"Product ID {product.id}: 저장 완료 (min: {amount_data.get('min_amount')}, max: {amount_data.get('max_amount')})")

        except json.JSONDecodeError as e:
            print(f"JSON 디코딩 오류 (Product ID {product.id}): {e}")
            product.savings_min_amount = None
            product.savings_max_amount = None
            product.save()

        except Exception as e:
            print(f"AI 파싱 오류 (Product ID {product.id}): {e}")
            product.savings_min_amount = None
            product.savings_max_amount = None
            product.save()

    print("AI 분석 및 업데이트 완료")

# preprocess_deposit_amounts_with_ai(DepositProducts.objects.all(), settings.GROQ_API_KEY1)
preprocess_deposit_amounts_with_ai(SavingsProducts.objects.all(), settings.GROQ_API_KEY2)