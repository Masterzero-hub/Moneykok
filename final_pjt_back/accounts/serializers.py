from rest_framework import serializers
from .models import User
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


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # 비밀번호는 제외

class UserInfoChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('email', 'password', 'name',)  # 수정할 수 없는 필드
        read_only_fields = ('email', 'password', 'name',)  # 읽기 전용 필드

