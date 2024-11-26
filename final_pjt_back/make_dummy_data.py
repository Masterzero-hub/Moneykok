import os
import django
import random
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
import json
from collections import OrderedDict
from datetime import timedelta, date
from django.core.management import call_command
from faker import Faker

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

from accounts.models import User
from deposits.models import DepositProducts
from savings.models import SavingsProducts

##### User 더미 데이터 생성 ######
# 랜덤 이름 생성 샘플
first_name_samples = "김이박최정강조윤장임신유한오서전황원문양손배백"
middle_name_samples = "민효세경서예지도하주윤채현지진승"
last_name_samples = "준윤우원호후서연아은진수혁영경환인"

def random_name():
    """랜덤 이름 생성"""
    return random.choice(first_name_samples) + random.choice(middle_name_samples) + random.choice(last_name_samples)

# 더미 데이터 생성 후 자동 로드
def generate_user_data(count=30):
    """
    현실적인 사용자 데이터를 생성하여 JSON으로 저장하고 로드합니다.
    나이, 성별, 소득(income)에 따른 데이터를 현실적으로 생성합니다.
    """
    users = []
    save_dir = 'fixtures/dummy_data/user_data.json'

    for i in range(count):
        user_data = OrderedDict()
        name = random_name()

        # 나이와 생년 계산
        current_year = now().year
        birth_year = random.randint(1970, 2005)  # 현실적인 생년 범위 (18~53세)
        age = current_year - birth_year

        # 성별에 따른 소득 범위 설정
        gender = random.choice(['남성', '여성'])
        if age < 25:
            income = random.randint(15, 30) * 100000  # 젊은 층 소득
        elif age < 35:
            income = random.randint(30, 50) * 100000  # 초기 경력 소득
        elif age < 50:
            income = random.randint(50, 100) * 100000  # 중장년층 소득
        else:
            income = random.randint(40, 80) * 100000  # 장년층 소득

        user_data["model"] = "accounts.User"
        user_data["pk"] = i + 1
        user_data["fields"] = {
            'email': f'user{i+1}@example.com',
            'name': name,
            'nickname': name,
            'phone': f'010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
            'gender': gender,
            'birthdate': f'{birth_year}-{random.randint(1, 12):02}-{random.randint(1, 28):02}',
            'income': income,  # 현실적인 소득
            'profile_description': "이 사용자에 대한 설명입니다.",
            'password': make_password("password1234!!"),  # 비밀번호 암호화
            'is_active': True,
            'date_joined': now().isoformat(),  # ISO 형식 시간
        }
        users.append(user_data)

    # JSON 파일로 저장
    os.makedirs(os.path.dirname(save_dir), exist_ok=True)
    with open(save_dir, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    print(f"User 더미 데이터 생성 완료: {save_dir}")
    load_fixture(save_dir)

fake = Faker('ko_KR')  # 한국어 로컬 설정

def generate_joined_data(data_type, count=50):
    """
    사용자 소득(income)을 기반으로 현실적인 JoinedDeposits 또는 JoinedSavings 더미 데이터를 생성합니다.
    
    :param data_type: 'deposits' 또는 'savings'
    :param count: 생성할 데이터 개수 (기본값: 50)
    """
    if data_type == 'deposits':
        model_name = "deposits.JoinedDeposits"
        products = list(DepositProducts.objects.all())
        save_dir = 'dummy_data/joined_deposits.json'
    elif data_type == 'savings':
        model_name = "savings.JoinedSavings"
        products = list(SavingsProducts.objects.all())
        save_dir = 'dummy_data/joined_savings.json'
    else:
        raise ValueError("data_type은 'deposits' 또는 'savings' 중 하나여야 합니다.")

    users = list(User.objects.all())

    if not users or not products:
        raise ValueError("User나 Product 데이터가 충분하지 않습니다.")

    os.makedirs(os.path.dirname(save_dir), exist_ok=True)
    data_list = []

    for i in range(count):
        user = random.choice(users)
        product = random.choice(products)

        # 소득 기반으로 적절한 가입 금액 설정
        income = user.income
        if income < 3000000:  # 소득이 낮은 경우
            save_amount = random.randint(500000, 3000000)  # 50만~300만 원
        elif income < 7000000:  # 중간 소득
            save_amount = random.randint(3000000, 10000000)  # 300만~1000만 원
        else:  # 고소득
            save_amount = random.randint(10000000, 50000000)  # 1000만~5000만 원

        save_trm = random.choice([6, 12, 24, 36])  # 가입 기간 (6~36개월)
        joined_date = now().date() - timedelta(days=random.randint(30, 365 * 3))
        expired_date = joined_date + timedelta(days=save_trm * 30)
        final_intr_rate = round(random.uniform(1.0, 5.0), 2)

        data = OrderedDict()
        data["model"] = model_name
        data["pk"] = i + 1
        data["fields"] = {
            "user": user.id,
            "product": product.id,
            "save_trm": save_trm,
            "save_amount": save_amount,
            "joined_date": str(joined_date),
            "expired_date": str(expired_date),
            "final_intr_rate": final_intr_rate,
        }
        data_list.append(data)

    with open(save_dir, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    print(f"더미 데이터 생성 완료: {save_dir}")
    load_fixture(save_dir)



def load_fixture(file_path):
    """JSON 파일을 Django 데이터베이스에 로드"""
    try:
        call_command('loaddata', file_path)
        print(f"데이터 로드 성공: {file_path}")
    except Exception as e:
        print(f"로딩 오류 {file_path}: {e}")

# 실행
if __name__ == "__main__":
    generate_user_data(count=500)
    generate_joined_data(data_type='deposits', count=1000)
    generate_joined_data(data_type='savings', count=1000)