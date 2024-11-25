import os
import django
from django.core.serializers import serialize

# Django 설정 초기화
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()


# 저장 디렉토리 지정 (필요 시 경로 수정)
output_dir = "fixtures"
os.makedirs(output_dir, exist_ok=True)

from deposits.models import DepositProducts, DepositSpecialCondition
from savings.models import SavingsProducts, SavingsSpecialCondition
from accounts.models import User
from communities.models import Article, Comment
from exchange.models import Exchange

def export_to_json(model, file_name=None):
    """
    특정 모델 데이터를 JSON 파일로 내보내는 함수

    Args:
        model: Django 모델 클래스
        file_name: 저장할 JSON 파일명 (기본값은 모델 이름을 사용)
    """
    # 모델 이름으로 기본 파일명 생성
    model_name = model.__name__
    file_name = file_name or f"{model_name.lower()}_data.json"

    # 모델 데이터 추출
    data = model.objects.all()
    json_data = serialize("json", data, indent=2)

    # 파일 경로 지정
    file_path = os.path.join(output_dir, file_name)

    # JSON 파일 저장
    with open(file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)
    print(f"{model_name} 데이터가 저장되었습니다: {file_path}")


#1 DepositSpecialCondition 데이터를 JSON으로 내보내기
# export_to_json(DepositSpecialCondition)

#2 SavingsSpecialCondition 데이터를 JSON으로 내보내기
# export_to_json(SavingsSpecialCondition)



# export_to_json(User)
# export_to_json(User)
# export_to_json(User)
# export_to_json(Article)
# export_to_json(Comment)
export_to_json(Exchange)