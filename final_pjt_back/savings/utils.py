import json
from django.db.models import Q
from django.http import JsonResponse
from .models import SavingsProducts

def filter_savings_products(filters):
    """
    필터링 로직을 처리하는 유틸 함수.
    filters: 딕셔너리 형태의 필터 조건 (ex. bank, conditions, join_term, amount)
    """
    products = SavingsProducts.objects.all()
    bank = filters.get('bank', None)  # 은행명 필터 (JSON 문자열 형태)
    conditions = filters.get('conditions', None)  # 우대조건 필터 (JSON 문자열 형태)
    join_term = filters.get('join_term', None)  # 가입 기간 필터
    amount = filters.get('amount', None)  # 가입금액 필터

    # 은행명 필터
    if bank:
        try:
            fin_co_no_list = json.loads(bank)  # JSON 문자열 -> Python 리스트 변환
            products = products.filter(bank__fin_co_no__in=fin_co_no_list)
        except json.JSONDecodeError:
            raise ValueError('fin_co_no는 유효한 JSON 배열이어야 합니다.')

    # 우대조건 필터
    if conditions:
        try:
            category_list = json.loads(conditions)  # JSON 문자열 -> Python 리스트 변환
            products = products.filter(
                Q(savingsspecialcondition__category__in=category_list) |
                Q(savingsspecialcondition__isnull=True)
            ).distinct()
        except json.JSONDecodeError:
            raise ValueError('special_condition_category는 유효한 JSON 배열이어야 합니다.')

    # 가입 기간 필터
    if join_term:
        try:
            join_term = int(join_term)
            products = products.filter(options__save_trm=join_term)
        except ValueError:
            raise ValueError('잘못된 가입 기간 값입니다.')

    # 가입금액 필터
    if amount:
        try:
            amount = int(amount)
            products = products.filter(
                Q(savings_min_amount__isnull=True, savings_max_amount__isnull=True) |
                Q(savings_min_amount__isnull=True, savings_max_amount__gte=amount) |
                Q(savings_max_amount__isnull=True, savings_min_amount__lte=amount) |
                Q(savings_min_amount__lte=amount, savings_max_amount__gte=amount)
            )
        except ValueError:
            raise ValueError('잘못된 가입금액 값입니다.')

    return products