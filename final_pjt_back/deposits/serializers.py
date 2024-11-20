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
