import os
import django
import random
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
import json
from collections import OrderedDict
from datetime import timedelta, date

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()
from django.conf import settings
from accounts.models import User
from deposits.models import DepositOptions, DepositProducts, Banks, DepositSpecialCondition, JoinedDeposits
from deposits.serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsSaveSerializer ,BanksSerializer, DepositProductsGETSerializer, DepositJoinSerializer, JoinedDepositSerializer
import requests

##### User 더미 데이터 생성 ######
# 랜덤 이름 생성 샘플
first_name_samples = "김이박최정강조윤장임신유한오서전황원문양손배백"
middle_name_samples = "민효세경서예지도하주윤채현지진승"
last_name_samples = "준윤우원호후서연아은진수혁영경환인"

def random_name():
    """랜덤 이름 생성"""
    return random.choice(first_name_samples) + random.choice(middle_name_samples) + random.choice(last_name_samples)


# 더미 데이터 생성
def generate_user_data(count=30):
    """User 더미 데이터를 JSON으로 저장"""
    users = []
    # JSON 파일 저장 경로
    save_dir = 'dummy_data/user_data.json'

    for i in range(count):
        user_data = OrderedDict()
        name = random_name()
        user_data["model"] = "accounts.User"
        user_data["pk"] = i + 1
        user_data["fields"] = {
            'email': f'user{i+1}@example.com',
            'name': name,
            'nickname': name,
            'phone': f'010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
            'gender': random.choice(['남성', '여성']),
            'birthdate': f'{random.randint(1950, 2005)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}',
            'income': random.randint(2000, 10000) * 1000,  # 소득 범위 설정
            'profile_description': "이 사용자에 대한 설명입니다.",
            'password': make_password("password1234!!"),  # 비밀번호 암호화
            'is_active': True,
            'date_joined': now().isoformat(),  # ISO 형식 시간
        }
        users.append(user_data)

    # JSON 파일로 저장
    os.makedirs(os.path.dirname(save_dir), exist_ok=True)  # 디렉토리 생성
    with open(save_dir, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    print(f"더미 데이터 생성 완료: {save_dir}")




# 더미 데이터 생성
def generate_joined_deposits_data(deposits_count=50):
    """JoinedDeposits 더미 데이터를 JSON으로 생성"""
    users = list(User.objects.all())  # 샘플 User 가져오기
    products = list(DepositProducts.objects.all())  # 샘플 Product 가져오기
    
    if not users or not products:
        raise ValueError("User나 DepositProducts 데이터가 충분하지 않습니다.")

    save_dir = 'dummy_data/joined_deposits.json'
    os.makedirs(os.path.dirname(save_dir), exist_ok=True)

    deposits = []

    for i in range(deposits_count):
        user = random.choice(users)
        product = random.choice(products)

        save_trm = random.choice([1, 3, 6, 12, 24, 36])  # 가입 기간(개월)
        save_amount = random.randint(1000000, 50000000)  # 가입 금액
        joined_date = now().date() - timedelta(days=random.randint(30, 365 * 3))  # 과거 3년 이내의 날짜
        expired_date = joined_date + timedelta(days=save_trm * 30)  # 가입 기간을 더하여 만기일 계산
        final_intr_rate = round(random.uniform(1.0, 5.0), 2)  # 저축 금리

        deposit_data = OrderedDict()
        deposit_data["model"] = "deposits.JoinedDeposits" 
        deposit_data["pk"] = i + 1
        deposit_data["fields"] = {
            "user": user.id,
            "product": product.id,
            "save_trm": save_trm,
            "save_amount": save_amount,
            "joined_date": str(joined_date),
            "expired_date": str(expired_date),
            "final_intr_rate": final_intr_rate,
        }
        deposits.append(deposit_data)

    # JSON 파일로 저장
    with open(save_dir, 'w', encoding='utf-8') as f:
        json.dump(deposits, f, ensure_ascii=False, indent=4)

    print(f"더미 데이터 생성 완료: {save_dir}")




# 실행
generate_user_data(count=30)  # 30개의 User 더미 데이터 생성


generate_joined_deposits_data(deposits_count=50) # 50개의 JoinedDeposits 더미 데이터 생성