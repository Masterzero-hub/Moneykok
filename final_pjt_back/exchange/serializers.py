from rest_framework import serializers
from .models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields =('cur_unit','cur_nm','deal_bas_r','ttb','tts')