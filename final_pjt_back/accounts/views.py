from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, EmailVerification
from .serializers import SignupSerializer, EmailVerificationSerializer
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# 인증 설정
from rest_framework.decorators import api_view, authentication_classes , permission_classes

# 권한 설정
from rest_framework.permissions import AllowAny


User = get_user_model()

def get_verification(email):
    """이메일에 해당하는 인증 정보를 가져오는 함수"""
    try:
        print(EmailVerification.objects.get(email=email, is_verified=False))
        return EmailVerification.objects.get(email=email, is_verified=False)
    except EmailVerification.DoesNotExist:
        print("오류")
        return None
    


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """회원가입 API"""
    serializer = SignupSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user_id': user.id,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def send_email(request):
    """이메일 인증 코드 발송"""
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': '이메일이 필요합니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 새로운 인증 정보 생성 또는 기존 정보 업데이트
        verification, _ = EmailVerification.objects.update_or_create(
            email=email,
            defaults={
                'verification_code': EmailVerification.generate_verification_code(),
                'is_verified': False,
                'expires_at': timezone.now() + timedelta(minutes=10)
            }
        )

        # 이메일 발송
        send_mail(
            subject='Moneykok 이메일 인증',
            message=f'''
            안녕하세요.
            요청하신 이메일 인증 코드입니다.

            인증 코드: {verification.verification_code}

            본 인증 코드는 10분 후 만료됩니다.
            '''.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({
            'message': '인증 코드가 발송되었습니다.',
            'expires_in': '10분'
        })
    
    except Exception as e:
        return Response({
            'error': '인증 코드 발송 중 오류가 발생했습니다.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def verify_email(request):
    """인증 코드 확인 및 이메일 인증 처리"""
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({"error": "이메일과 인증 코드는 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)

    verification = get_verification(email)
    if not verification:
        return Response({
            'error': '인증 정보를 찾을 수 없습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if verification.is_expired:
        return Response({
            'error': '인증 코드가 만료되었습니다. 새로운 인증 코드를 요청해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    if verification.verification_code != code:
        return Response({
            'error': '잘못된 인증 코드입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    verification.is_verified = True
    verification.save()

    return Response({
        'message': '이메일이 성공적으로 인증되었습니다.',
        'verified': True
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def resend_email(request):
    """이메일 인증 코드 재발송 뷰"""
    email = request.data.get("email")
    if not email:
        return Response({"message": "이메일은 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 기존 인증 코드가 있으면 새로운 인증 코드 발송
        verification = get_verification(email)
        if not verification:
            return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 인증 코드 재생성 및 발송
        verification.verification_code = EmailVerification.generate_verification_code()
        verification.expires_at = timezone.now() + timedelta(minutes=10)
        verification.save()

        # 이메일 발송
        send_mail(
            subject='Moneykok 이메일 인증',
            message=f'''
                안녕하세요.
                요청하신 이메일 인증 코드입니다.

                인증 코드: {verification.verification_code}

                본 인증 코드는 10분 후 만료됩니다.
            '''.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "인증 코드가 재발송되었습니다."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": f"오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)