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
from groq import Groq



def preprocess_spcl_cnd_with_ai(spcl_cnd_text, API_KEY):
    api_key = API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")
    client = Groq(api_key=api_key)
    processed_spcl_cnd =""
    prompt = f"""다음 텍스트는 금융 상품의 우대조건을 포함하고 있습니다. 아래의 규칙에 따라 각 조건을 세부적으로 분리하고, 명확히 출력하세요. 조건은 한 개일 수도 있으니 반드시 조건의 수에 관계없이 처리 규칙을 준수하여 출력해야 합니다.

#### 처리 규칙
0. 조건이 나뉘지 않고, 줄글로 나올 수 있습니다.
1. "▶", "-" 등의 기호는 각 조건을 나누는 구분자로 간주하고, 이를 기준으로 조건을 분리하세요.
2. ①, ②, ③, ⑤, ⑤와 같은 기호는 숫자(1, 2, 3, 4, 5, ...)로 변환하세요.
3. 보너스이율과 우대금리는 같은 개념으로 간주하며, 금리는 반드시 X.XX% 형식으로 변환하세요. 금리가 없는 조건은 금리를 표시하지 마세요.
4. "최고 우대금리"와 관련된 설명은 모두 제외하세요.
5. 동일한 조건에 여러 금액 범위가 있을 경우, 금액 범위별로 조건을 각각 독립된 항목으로 세분화하세요.
6. 모든 조건의 세부 내용을 포함하되, 불필요한 설명 문구(예: "우대 조건은 다음과 같습니다")는 제외하고 조건만 출력하세요.

#### 입력 텍스트
{spcl_cnd_text}

#### 출력 형식
1. 우대 조건 설명 - X.XX%
2. 우대 조건 설명 - X.XX%
...

#### 주의사항
- 출력 형식만 반환하고,  출력 형식에 맞게 알맞은 내용으로 출력해야합니다. 매우 중요합니다.!!!!
- 각 조건은 독립된 항목으로 출력하세요. !!!!!!
- 모든 세부 조건을 포함하여 내용을 누락하지 마세요. !!!!
- 입력 텍스트 내 금리와 조건 정보를 정확히 추출하고, 규칙에 따라 변환하세요. 매우중요합니다!!!!
        """
    try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "당신은 금융 데이터 전처리 전문가입니다."},
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.2-90b-text-preview",
                temperature=0.2,
                max_tokens=4096,
                top_p=0.9,
            )
            processed_spcl_cnd = response.choices[0].message.content.strip()
    except Exception as e:
            print(f"AI 파싱 오류")
    return processed_spcl_cnd

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
            if any(keyword in spcl_cnd for keyword in ['우대조건 없음', '해당사항 없음', '없음', '해당무', '우대조건 없이']):
                processed_spcl_cnd = None
            else:
                processed_spcl_cnd = preprocess_spcl_cnd_with_ai(spcl_cnd, settings.GROQ_API_KEY1)
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
                    'processed_spcl_cnd':processed_spcl_cnd,
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
    URL = settings.DEPOSIT_URL + 'savingProductsSearch.json'
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
            if any(keyword in spcl_cnd for keyword in ['우대조건 없음', '해당사항 없음', '없음', '해당무', '우대조건 없이']):
                processed_spcl_cnd = None
            else:
                processed_spcl_cnd = preprocess_spcl_cnd_with_ai(spcl_cnd, settings.GROQ_API_KEY2)
                
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

            if not SavingsProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                save_data_P = {
                    'fin_prdt_cd': fin_prdt_cd,
                    'fin_prdt_nm': fin_prdt_nm,
                    'etc_note': etc_note,
                    'join_deny': join_deny,
                    'join_member': join_member,
                    'join_way': join_way,
                    'spcl_cnd': spcl_cnd,
                    'processed_spcl_cnd':processed_spcl_cnd,
                }
    

                serializerProducts = SavingsProductsSaveSerializer(data=save_data_P)
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