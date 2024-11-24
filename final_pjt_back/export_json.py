import os
import django

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

from deposits.models import DepositSpecialCondition
from savings.models import SavingsSpecialCondition
from django.core.serializers import serialize

# 저장 디렉토리 지정 (필요 시 경로 수정)
output_dir = "fixtures"
os.makedirs(output_dir, exist_ok=True)

def export_to_json():
    """
    DepositSpecialCondition 및 SavingsSpecialCondition 데이터를 JSON 파일로 내보냄
    """
    # DepositSpecialCondition 데이터 추출 및 저장
    deposit_conditions = DepositSpecialCondition.objects.all()
    deposit_json = serialize("json", deposit_conditions, indent=2)
    deposit_file_path = os.path.join(output_dir, "deposits_special_conditions.json")
    with open(deposit_file_path, "w", encoding="utf-8") as deposit_file:
        deposit_file.write(deposit_json)
    print(f"DepositSpecialCondition 데이터가 저장되었습니다: {deposit_file_path}")

    # SavingsSpecialCondition 데이터 추출 및 저장
    savings_conditions = SavingsSpecialCondition.objects.all()
    savings_json = serialize("json", savings_conditions, indent=2)
    savings_file_path = os.path.join(output_dir, "savings_special_conditions.json")
    with open(savings_file_path, "w", encoding="utf-8") as savings_file:
        savings_file.write(savings_json)
    print(f"SavingsSpecialCondition 데이터가 저장되었습니다: {savings_file_path}")

# 함수 실행
export_to_json()