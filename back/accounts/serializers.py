from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'gender', 'birthdate', 'income', 'password']

    def create(self, validated_data):
        # 비밀번호 암호화를 위해 create_user 메서드 사용
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate'],
            income=validated_data['income'],
            password=validated_data['password']
        )
        return user
    
