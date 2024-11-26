from django.db import models
from deposits.models import Banks
# Create your models here.
class SavingsProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    bank = models.ForeignKey("deposits.Banks", on_delete=models.CASCADE)  # 은행과의 외래 키 관계
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField()  # 금융 상품 설명
    join_deny = models.IntegerField()  # 가입 제한 (1: 제한없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField()  # 우대 조건
    processed_spcl_cnd = models.TextField(null=True, blank=True)  # 가공된 우대 조건
    savings_min_amount = models.IntegerField(null=True, blank=True)  # 최소 금액(만원)
    savings_max_amount = models.IntegerField(null=True, blank=True)  # 최대 금액(만원)


class SavingsOptions(models.Model):
    product = models.ForeignKey("SavingsProducts", on_delete=models.CASCADE, related_name='options')  # 적금 상품과의 외래 키 관계
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리 유형명
    intr_rate = models.FloatField()  # 저축금리
    intr_rate2 = models.FloatField()  # 최고 우대금리
    save_trm = models.IntegerField()  # 저축기간 (단위: 개월)


class SavingsSpecialCondition(models.Model):
    product = models.ForeignKey("SavingsProducts", on_delete=models.CASCADE)  # 적금 상품과의 외래 키 관계
    category = models.CharField(
        max_length=20,
        choices=[
            ('거래 연동', '거래 연동'),
            ('사용 실적', '사용 실적'),
            ('신규 가입', '신규 가입'),
            ('비대면/모바일 뱅킹', '비대면/모바일 뱅킹'),
            ('마케팅 및 기타 동의', '마케팅 및 기타 동의'),
            ('기타', '기타'),
        ]
    )
    condition_content = models.TextField()
    prime_rate = models.FloatField()  # 우대금리


class JoinedSavings(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)  # User 모델과 외래키
    product = models.ForeignKey("SavingsProducts", on_delete=models.CASCADE, related_name='joined_product')  # 적금 상품과의 외래 키 관계
    save_trm = models.IntegerField()  # 가입 기간
    save_amount = models.IntegerField()  # 가입 금액
    joined_date = models.DateField(auto_now=True)  # 가입한 날짜
    expired_date = models.DateField()  # 만기일
    final_intr_rate = models.FloatField()  # 저축금리