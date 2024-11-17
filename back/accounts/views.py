from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import SignupSerializer

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    if not email:
        return Response({"message": "이메일은 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, email=email)
    
    # 이메일 인증 여부 확인
    if not user.is_verified:
        return Response({"message": "이메일 인증이 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SignupSerializer(user, data=request.data, partial=True)  # partial=True로 수정
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입이 완료되었습니다!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_email(request):
    """이메일 인증 코드 발송 뷰"""
    email = request.data.get('email')
    if not email:
        return Response({"message": "이메일은 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "name": "기본이름",
            "nickname": "기본닉네임",
            "gender": "M",  # 기본값 설정 (필요에 따라 수정 가능)
            "birthdate": "1990-01-01",  # 기본값
            "income": 100,
        }
    )
    
    # 이미 인증된 사용자라면 코드 발송 중지
    if user.is_verified:
        return Response({"message": "이미 이메일 인증이 완료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

    user.generate_verification_code()
    return Response({"message": "이메일 인증 코드가 발송되었습니다."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    code = request.data.get('code')
    if not email or not code:
        return Response({"message": "이메일과 인증 코드는 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, email=email)
    
    if user.verify_code(code):
        return Response({"message": "이메일 인증 성공!"}, status=status.HTTP_200_OK)
    
    return Response({"message": "인증 코드가 잘못되었거나 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resend_email(request):
    """이메일 인증 코드 재발송 뷰"""
    email = request.data.get("email")
    if not email:
        return Response({"message": "이메일은 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_object_or_404(User, email=email)

        # 이메일 인증 여부 확인
        if user.is_verified:
            return Response({"message": "이미 이메일 인증이 완료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 인증 코드 재생성 및 발송
        user.generate_verification_code()
        return Response({"message": "인증 코드가 재발송되었습니다."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": f"오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
