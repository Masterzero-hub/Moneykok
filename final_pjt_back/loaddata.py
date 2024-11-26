import os
import django
from django.core.management import call_command
# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()
def load_data(directory="fixtures"):
    """
    주어진 디렉토리에서 모든 JSON 파일을 읽어 Django 데이터베이스에 로드
    """
    if not os.path.exists(directory):
        print(f"폴더 {directory}가 존재하지 않습니다.")
        return
    # 디렉토리 내 모든 파일 순회
    for filename in os.listdir(directory):
        if filename.endswith(".json"):  # JSON 파일만 선택
            file_path = os.path.join(directory, filename)
            try:
                print(f"Loading fixture: {file_path}")
                call_command('loaddata', file_path)  # loaddata 명령어 실행
                print(f"Successfully loaded: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

if __name__ == "__main__":
    load_data("fixtures/banks_products_data")
    load_data("fixtures/options_data")
    load_data("fixtures/dummy_data")
    load_data()