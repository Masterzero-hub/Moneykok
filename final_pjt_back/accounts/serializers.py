from rest_framework import serializers
from .models import User, EmailVerification
from django.core.exceptions import ValidationError
from django.utils import timezone


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'nickname', 'phone', 'gender', 'birthdate', 'income']

    def validate_email(self, value):
        """이메일 중복 확인"""
        if User.objects.filter(email=value).exists():
            raise ValidationError("이미 가입된 이메일입니다.")
        return value

    def create(self, validated_data):
        """회원가입 처리"""
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)

    class Meta:
        model = EmailVerification
        fields = ['email', 'code']

    def validate_code(self, value):
        """인증 코드 검증"""
        email = self.initial_data.get('email')
        verification = EmailVerification.objects.filter(email=email).first()

        if not verification:
            raise ValidationError("이메일 인증이 필요합니다.")
        
        if verification.is_verified:
            raise ValidationError("이미 이메일 인증이 완료되었습니다.")
        
        if verification.is_expired:
            raise ValidationError("인증 코드가 만료되었습니다. 새로운 인증 코드를 요청해주세요.")
        
        if verification.verification_code != value:
            raise ValidationError("잘못된 인증 코드입니다.")
        
        return value

    def update(self, instance, validated_data):
        """이메일 인증 처리"""
        instance.is_verified = True
        instance.save()
        return instance