from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail, BadHeaderError

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

    def create_superuser(self, email, password=None, **extra_fields):
        """슈퍼유저 생성 메서드"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("슈퍼유저는 is_staff=True여야 합니다.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("슈퍼유저는 is_superuser=True여야 합니다.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="이메일")
    is_verified = models.BooleanField(default=False, verbose_name="이메일 인증 여부")
    name = models.CharField(max_length=20, verbose_name="이름")
    nickname = models.CharField(max_length=20, unique=True, verbose_name="닉네임")
    gender = models.CharField(max_length=1, choices=[("M", "남성"), ("F", "여성")], verbose_name="성별")
    birthdate = models.DateField(verbose_name="생년월일")
    income = models.IntegerField(verbose_name="소득")
    is_active = models.BooleanField(default=True, verbose_name="활성 상태")
    is_staff = models.BooleanField(default=False, verbose_name="스태프 권한")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="가입일")


    email_verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="이메일 인증 코드")
    email_verification_expiry = models.DateTimeField(blank=True, null=True, verbose_name="인증 코드 만료 시간")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname', 'birthdate']

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def generate_verification_code(self):
        """6자리 인증 코드 생성 및 이메일 발송"""
        code = f"{random.randint(100000, 999999)}"
        self.email_verification_code = code
        self.email_verification_expiry = timezone.now() + timedelta(minutes=10)
        self.save()

        try:
            send_mail(
                "이메일 인증 코드",
                f"인증 코드는 {code}입니다. 10분 내로 인증을 완료해주세요.",
                "dlsdud0704@gmail.com",
                [self.email],
            )
        except BadHeaderError:
            raise ValueError("잘못된 이메일 헤더로 인해 인증 코드를 발송할 수 없습니다.")

    def verify_code(self, code):
        """인증 코드 확인"""
        if (
            self.email_verification_code == code and
            self.email_verification_expiry > timezone.now()
        ):
            self.is_verified = True  # 인증 완료 상태
            self.email_verification_code = None
            self.email_verification_expiry = None
            self.save()
            return True
        return False