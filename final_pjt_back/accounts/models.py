from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """일반 사용자 생성 메서드"""
        if not email:
            raise ValueError("이메일은 필수 항목입니다.")
        email = self.normalize_email(email)  # 이메일 주소 정규화
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 암호화 저장
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=20, verbose_name="이름")
    nickname = models.CharField(max_length=20, unique=True, verbose_name="닉네임")
    phone = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="전화번호",
        validators=[
            RegexValidator(
                regex=r"\d{3}-\d{4}-\d{4}$",  # 11자리 숫자만 허용
                message="전화번호는 010-1234-5678형식이어야 합니다."
            )
        ]
    )
    gender = models.CharField(max_length=2, verbose_name="성별")
    birthdate = models.DateField(verbose_name="연도")
    income = models.IntegerField(verbose_name="소득")
    is_active = models.BooleanField(default=True, verbose_name="활성 상태")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="가입일")
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class EmailVerification(models.Model):
    email = models.EmailField(db_index=True)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_verification')
        ]

    def __str__(self):
        return f"{self.email} - {'인증완료' if self.is_verified else '미인증'}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_verification_code(cls):
        """6자리 랜덤 숫자 생성"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
