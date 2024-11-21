from rest_framework import serializers
from .models import DepositOptions, DepositProducts, DepositSpecialCondition, Banks


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields ="__all__"

class DepositProductsSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields =('fin_prdt_cd','fin_prdt_nm','etc_note','join_deny', 'join_member', 'join_way', 'spcl_cnd',)
        read_only_fields = ('bank',)

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields ="__all__"
        read_only_fields = ('bank',)

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields ="__all__"
        read_only_fields = ('product',)


class DepositSpecialConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositSpecialCondition
        fields = ('category', 'condition_title','condition_content','prime_rate')
        read_only_fields = ('product',)


class DepositProductsGETSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(read_only=True)  # 은행 정보를 포함
    options = DepositOptionsSerializer(many=True, read_only=True)  # 옵션 정보를 포함
    special_conditions = DepositSpecialConditionSerializer(many=True, read_only=True, source='depositspecialcondition_set')

    class Meta:
        model = DepositProducts
        fields = [
            'id',          # 기본 키
            'fin_prdt_cd', # 금융 상품 코드
            'bank',        # 외래 키: 은행 정보
            'fin_prdt_nm', # 금융 상품명
            'etc_note',    # 기타 설명
            'join_deny',   # 가입 제한
            'join_member', # 가입 대상
            'join_way',    # 가입 방법
            'spcl_cnd',    # 우대 조건
            'deposit_min_amount',
            'deposit_max_amount',
            'options',     # 옵션 정보
            'special_conditions' # 우대 조건 상세 정보
        ]