from rest_framework import serializers
from .models import DepositOptions, DepositProducts, Banks

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

class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields ="__all__"

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = [
            'id', 'fin_prdt_cd', 'bank',  # 은행 정보를 원하는 위치에 배치
            'fin_prdt_nm', 'etc_note',
            'join_deny', 'join_member', 'join_way', 'spcl_cnd',
            
            'options'  # 옵션 정보를 원하는 위치에 배치
        ]
    bank = BanksSerializer(read_only=True)  # 은행 정보를 포함
    options = DepositOptionsSerializer(many=True, read_only=True)  # 옵션 정보를 포함