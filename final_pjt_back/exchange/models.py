from django.db import models

class Exchange(models.Model):
    cur_unit = models.CharField(max_length=100)  # 통화 단위 (예: 'USD', 'EUR', 'AED' 등)
    cur_nm = models.CharField(max_length=100)    # 통화 이름 (한글 표기, 예: '아랍에미리트 디르함')
    ttb = models.CharField(max_length=100)       # 전신환 매입률 (TTB, 은행이 외화를 살 때의 환율)
    tts = models.CharField(max_length=100)       # 전신환 매도율 (TTS, 은행이 외화를 팔 때의 환율)
    deal_bas_r = models.CharField(max_length=100)  # 매매 기준율 (거래의 기준이 되는 환율)