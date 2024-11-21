from rest_framework import serializers
from .models import DepositOptions, DepositProducts, Banks


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields ="__all__"

class DepositProductsSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(read_only=True)
    class Meta:
        model = DepositProducts
        fields ="__all__"
        # read_only_fields = ('bank',)

class DepositOptionsSerializer(serializers.ModelSerializer):
    product = DepositProductsSerializer(read_only=True)
    class Meta:
        model = DepositOptions
        fields ="__all__"
        # read_only_fields = ('product',)
        

class DepositProductsSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(read_only=True)  # 은행 정보를 포함
    options = DepositOptionsSerializer(many=True, read_only=True)  # 옵션 정보를 포함

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
            'options'      # 옵션 정보
        ]