from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.response import Response
import requests
from rest_framework import status
from django.utils import timezone
from .models import Exchange
from .serializers import ExchangeSerializer

# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def exchange(request):
    if request.method == "GET":
        EXCHANGE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        params = {
            'authkey': settings.EXCHANGE_API_KEY,
            'searchdate': timezone.now().strftime('%Y%m%d'),
            # 'searchdate': '20241122',
            'data': 'AP01'
        }

        try:
            # 외부 API 호출
            response = requests.get(EXCHANGE_URL, params=params)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            exchange_data = response.json()

            # 기존 데이터 삭제 (옵션)
            Exchange.objects.all().delete()

            # 새로운 데이터 저장
            for data in exchange_data:
                serializer = ExchangeSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # 외부 API에서 가져온 데이터 반환
            return Response(exchange_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException:
            # 외부 API 호출 실패 시, DB에서 데이터 조회 및 반환
            saved_data = Exchange.objects.all()
            if saved_data.exists():
                serializer = ExchangeSerializer(saved_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # DB에도 데이터가 없을 경우 에러 반환
                return Response(
                    {'error': '외부 API 호출과 로컬 데이터 조회 모두 실패했습니다.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    if request == "POST":
        pass