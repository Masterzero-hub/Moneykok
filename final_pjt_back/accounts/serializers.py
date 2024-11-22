from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth.password_validation import validate_password

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'nickname', 'phone', 'gender', 'birthdate', 'income']

    def validate_password(self, value):
        """비밀번호 검증"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate_email(self, value):
        """이메일 중복 확인"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")
        return value

    def create(self, validated_data):
        """회원가입 처리"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'phone', 'gender', 'birthdate', 'income']
        exclude = ('password',)  # 비밀번호는 제외

class UserInfoChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'phone', 'gender', 'birthdate', 'income']
        exclude = ('email', 'password', 'name',)  # 수정할 수 없는 필드
        read_only_fields = ('email', 'password', 'name',)  # 읽기 전용 필드

