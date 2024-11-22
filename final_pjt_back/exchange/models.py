from django.db import models

class Exchange(models.Model):
    cur_unit = models.CharField(max_length=100)  # 통화 단위 (예: 'USD', 'EUR', 'AED' 등)
    cur_nm = models.CharField(max_length=100)    # 통화 이름 (한글 표기, 예: '아랍에미리트 디르함')
    ttb = models.CharField(max_length=100)       # 전신환 매입률 (TTB, 은행이 외화를 살 때의 환율)
    tts = models.CharField(max_length=100)       # 전신환 매도율 (TTS, 은행이 외화를 팔 때의 환율)
    deal_bas_r = models.CharField(max_length=100)  # 매매 기준율 (거래의 기준이 되는 환율)
    bkpr = models.CharField(max_length=100)      # 장부 환율 (기준 환율로 사용됨)
    yy_efee_r = models.CharField(max_length=100)  # 연간 환전 수수료율 (0이면 수수료 없음)
    ten_dd_efee_r = models.CharField(max_length=100)  # 10일 기준 환전 수수료율 (0이면 수수료 없음)
    kftc_deal_bas_r = models.CharField(max_length=100)  # 금융통화위원회 기준 매매 환율
    kftc_bkpr = models.CharField(max_length=100)       # 금융통화위원회 기준 장부 환율
