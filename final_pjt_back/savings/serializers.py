from rest_framework import serializers
from .models import SavingsOptions, SavingsProducts, SavingsSpecialCondition, Banks, JoinedSavings

class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = "__all__"

class SavingsProductsSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProducts
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'etc_note', 'join_deny', 'join_member', 'join_way', 'spcl_cnd',)
        read_only_fields = ('bank',)

class SavingsProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProducts
        fields = "__all__"
        read_only_fields = ('bank',)

class SavingsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsOptions
        fields = "__all__"
        read_only_fields = ('product',)


class SavingsSpecialConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsSpecialCondition
        fields = ('category', 'condition_title', 'condition_content', 'prime_rate')
        read_only_fields = ('product',)


class SavingsProductsGETSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(read_only=True)  # 은행 정보를 포함
    options = SavingsOptionsSerializer(many=True, read_only=True)  # 옵션 정보를 포함
    special_conditions = SavingsSpecialConditionSerializer(many=True, read_only=True, source='savingsspecialcondition_set')
    final_intr_rate = serializers.FloatField(read_only=True)  # 최종 금리 필드 추가

    class Meta:
        model = SavingsProducts
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
            'savings_min_amount',
            'savings_max_amount',
            'options',     # 옵션 정보
            'final_intr_rate',   # 최종 금리 필드
            'special_conditions', # 우대 조건 상세 정보
        ]

class JoinedSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedSavings
        fields = ['save_amount', 'save_trm', 'joined_date', 'expired_date', 'final_intr_rate']

class SavingsJoinSerializer(serializers.ModelSerializer):
    product = SavingsProductsGETSerializer(read_only=True)  # 적금 상품 상세 정보

    class Meta:
        model = JoinedSavings
        fields = ('user', 'product', 'save_trm', 'save_amount', 'joined_date', 'expired_date', 'final_intr_rate')
        read_only_fields = ('user', 'product')
        
class JoinedSavingsDetailedSerializer(serializers.ModelSerializer):
    bank = BanksSerializer(source='product.bank', read_only=True)
    product = SavingsProductsSaveSerializer(read_only=True)

    class Meta:
        model = JoinedSavings
        fields = [
            'user',
            'bank',
            'product',
            'save_amount',
            'save_trm',
            'joined_date',
            'expired_date',  # 추가
            'final_intr_rate'
        ]
