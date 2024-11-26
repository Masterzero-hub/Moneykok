from rest_framework import serializers
from .models import DepositOptions, DepositProducts, DepositSpecialCondition, Banks, JoinedDeposits

class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields ="__all__"

class DepositProductsSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = "__all__"
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
        fields = "__all__"
        read_only_fields = ('product',)


class DepositProductsGETSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(read_only=True)  # 은행 정보를 포함
    options = DepositOptionsSerializer(many=True, read_only=True)  # 옵션 정보를 포함
    special_conditions = DepositSpecialConditionSerializer(many=True, read_only=True, source='depositspecialcondition_set')
    final_intr_rate = serializers.FloatField(read_only=True)  # 최종 금리 필드 추가

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
            'final_intr_rate',   # 최종 금리 필드
            'special_conditions', # 우대 조건 상세 정보
        ]

class JoinedDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedDeposits
        fields = ['save_amount', 'save_trm', 'joined_date', 'expired_date', 'final_intr_rate']

class DepositJoinSerializer(serializers.ModelSerializer):
    product = DepositProductsGETSerializer(read_only=True)  # 예금 상품 상세 정보

    class Meta:
        model = JoinedDeposits
        fields = ('user', 'product', 'save_trm', 'save_amount', 'joined_date', 'expired_date', 'final_intr_rate')
        read_only_fields = ('user', 'product')
        
class JoinedDepositSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(source='product.bank', read_only=True)
    product = DepositProductsSaveSerializer(read_only=True)

    class Meta:
        model = JoinedDeposits
        fields = [
            'id',          # 기본 키
            'user',
            'bank',
            'product',
            'save_amount',
            'save_trm',
            'joined_date',
            'expired_date',  # 추가
            'final_intr_rate'
        ]