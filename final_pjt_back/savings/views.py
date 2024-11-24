from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from django.db.models import Q, Count, Max, Subquery, OuterRef

from .models import SavingsOptions, SavingsProducts, JoinedSavings
from .serializers import (
    SavingsProductsGETSerializer,
    SavingsJoinSerializer,
    JoinedSavingsDetailedSerializer,
)
from .utils import filter_savings_products

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
# 적금상품 상세조회
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def savings_detail(request, fin_prdt_cd):
    try:
        # 적금 상품 가져오기
        savings = get_object_or_404(SavingsProducts, fin_prdt_cd=fin_prdt_cd)
        
        # 직렬화 후 반환
        serializer = SavingsProductsGETSerializer(savings, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        # 기타 예외 처리
        return JsonResponse({'message': '적금 상품 정보를 가져오는 중 오류가 발생했습니다.', 'error': str(e)}, status=500)

# 적금 상품 조회
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def savings_list(request):
    try:
        # GET 요청 데이터를 필터로 전달
        filters = {key: (None if value in ['', [], '0'] else value) for key, value in request.GET.items()}
        products = filter_savings_products(filters)  # 필터링 함수 호출
    except ValueError as e:
        return JsonResponse({'message': '조건에 맞는 데이터가 없습니다.', 'error': str(e)}, status=400)
    
    # `save_trm=12` 조건의 최고 금리 가져오기
    options_with_save_trm_12 = SavingsOptions.objects.filter(
        product=OuterRef('pk'), save_trm=12
    ).order_by('-intr_rate2')

    # fallback: 가장 마지막 `intr_rate2` 데이터 가져오기
    fallback_option = SavingsOptions.objects.filter(
        product=OuterRef('pk')
    ).order_by('-id')

    # `save_trm=12`의 `intr_rate2`와 fallback 값을 결합하여 최종 금리 결정
    products = products.annotate(
        selected_intr_rate=Subquery(
            options_with_save_trm_12.values('intr_rate2')[:1]  # `save_trm=12` 금리
        )
    ).annotate(
        fallback_intr_rate=Subquery(
            fallback_option.values('intr_rate2')[:1]  # fallback 금리
        )
    ).annotate(
        final_intr_rate=Max('selected_intr_rate', 'fallback_intr_rate')  # 최종 금리
    )

    products = products.order_by('-final_intr_rate')

    # 조건에 맞는 데이터가 없을 경우 처리
    if not products.exists():
        return JsonResponse({'message': '조건에 맞는 데이터가 없습니다.', 'data': []}, status=404)

    # 직렬화 후 응답
    serializer = SavingsProductsGETSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

##### 상품 가입하기 #####
@api_view(['POST'])
def savings_join(request, fin_prdt_cd):
    try:
        # 로그인된 사용자
        user = request.user

        # 적금 상품 정보 가져오기
        try:
            product = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        except SavingsProducts.DoesNotExist:
            return Response({'error': '해당 상품이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 요청 데이터 가져오기
        save_trm = request.data.get('save_trm')  # 가입 기간 (개월)
        save_amount = request.data.get('save_amount')  # 가입 금액 (만 원 단위)
        final_intr_rate = request.data.get('final_intr_rate')  # 사용자 요청 금리

        if not save_trm or not save_amount or final_intr_rate is None:
            return Response({'error': '가입 기간(save_trm), 금액(save_amount), 금리(final_intr_rate)를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 입력 값 검증
        try:
            save_trm = int(save_trm)
            save_amount = int(save_amount) * 10000
            final_intr_rate = float(final_intr_rate)
        except ValueError:
            return Response({'error': '입력 값은 숫자 형식이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 최소 및 최대 가입 금액 확인
        savings_min_amount = product.savings_min_amount or 0
        savings_max_amount = product.savings_max_amount

        if save_amount < savings_min_amount:
            return Response({'error': f'가입 금액은 최소 {savings_min_amount}원 이상이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if savings_max_amount and save_amount > savings_max_amount:
            return Response({'error': f'가입 금액은 최대 {savings_max_amount}원을 초과할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 적합한 옵션 필터링 (기간만 확인)
        valid_options = [
            option for option in product.options.all()
            if option.save_trm == save_trm
        ]

        if not valid_options:
            return Response({'error': f'{save_trm}개월에 해당하는 옵션이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 만기일 계산
        try:
            expired_date = now().date() + relativedelta(months=save_trm)
        except Exception as e:
            return Response({'error': f'만기일 계산 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 데이터 저장
        joined_savings = JoinedSavings.objects.create(
            user=user,
            product=product,
            save_trm=save_trm,
            save_amount=save_amount,
            expired_date=expired_date,
            final_intr_rate=final_intr_rate
        )

        # 결과 반환
        serializer = SavingsJoinSerializer(joined_savings)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': f'서버 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 가입한 상품 목록 보여주기
@api_view(["GET"])
def joined_savings(request):
    try:
        user = request.user
        # 특정 사용자의 가입 데이터를 가져옴
        joined_products = JoinedSavings.objects.filter(user=user)

        if not joined_products.exists():
            return Response({"message": "No subscriptions found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # 만기일 기준으로 정렬
        joined_products = sorted(joined_products, key=lambda x: x.expired_date)

        # 직렬화
        serializer = JoinedSavingsDetailedSerializer(joined_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'서버 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def recommend_products(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': '로그인이 필요합니다.'}, status=401)

    # Step 0: 필터링된 상품 가져오기
    try:
        filters = {key: (None if value in ['', [], '0'] else value) for key, value in request.GET.items()}
        filtered_products = filter_savings_products(filters)  # 필터링 함수 호출
    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    # Step 1: 유사 사용자 찾기
    user_data = np.array([[user.income, user.birthdate.year, 1 if user.gender == '남성' else 0]])
    all_users = User.objects.exclude(id=user.id)

    similar_users = []
    for other_user in all_users:
        other_data = np.array([[other_user.income, other_user.birthdate.year, 1 if other_user.gender == '남성' else 0]])
        similarity = cosine_similarity(user_data, other_data)
        similar_users.append((other_user, similarity[0][0]))

    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:10]
    similar_user_ids = [u[0].id for u in similar_users]

    # Step 2: 유사 사용자가 가입한 상품 가져오기
    joined_savings = JoinedSavings.objects.filter(user_id__in=similar_user_ids)

    # 상품별 점수 계산
    product_scores = (
        joined_savings
        .values('product_id')
        .annotate(score=Count('product_id'))
        .order_by('-score')
    )

    # 상위 3개 추천
    recommended_product_ids = [p['product_id'] for p in product_scores[:3]]
    recommended_products = filtered_products.filter(id__in=recommended_product_ids)

    # Step 3: 직렬화 및 응답 반환
    serializer = SavingsProductsGETSerializer(recommended_products, many=True)
    return Response({'recommended_products': serializer.data})