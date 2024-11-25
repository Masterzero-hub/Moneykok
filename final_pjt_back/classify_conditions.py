import os
import django

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

import json
import re
from django.conf import settings
from dotenv import load_dotenv
from groq import Groq

from deposits.models import DepositProducts, DepositSpecialCondition
from savings.models import SavingsProducts, SavingsSpecialCondition

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
            model="llama-3.2-90b-vision-preview",
            temperature=0,
            max_tokens=4096,
            
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

def analyze_conditions(products, product_type):
    """
    주어진 상품 목록의 우대조건 데이터를 분석.
    """
    for product in products:
        spcl_cnd = product.spcl_cnd.strip()
        if spcl_cnd and spcl_cnd not in ['우대조건 없음', '해당사항 없음', '없음']:
            parsed_conditions = parse_special_conditions(spcl_cnd)
            for condition in parsed_conditions:
                # 공통 저장 로직
                if condition.get('prime_rate') is None:
                    print(f"prime_rate가 없어 저장하지 않음: {condition}")
                    continue
                
                if product_type == "deposits":
                    if not DepositSpecialCondition.objects.filter(
                        product=product,
                        **condition
                    ).exists():
                        DepositSpecialCondition.objects.create(product=product, **condition)
                elif product_type == "savings":
                    if not SavingsSpecialCondition.objects.filter(
                        product=product,
                        **condition
                    ).exists():
                        SavingsSpecialCondition.objects.create(product=product, **condition)
    print(f"{product_type.capitalize()} 저장 완료")

# 실행 로직
deposits_products = DepositProducts.objects.all()
savings_products = SavingsProducts.objects.all()

analyze_conditions(deposits_products, "deposits")
analyze_conditions(savings_products, "savings")
