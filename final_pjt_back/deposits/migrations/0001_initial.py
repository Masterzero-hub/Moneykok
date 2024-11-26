# Generated by Django 4.2.4 on 2024-11-26 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.CharField(max_length=7)),
                ('kor_co_nm', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('processed_spcl_cnd', models.TextField(blank=True, null=True)),
                ('deposit_min_amount', models.IntegerField(blank=True, null=True)),
                ('deposit_max_amount', models.IntegerField(blank=True, null=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deposits.banks')),
            ],
        ),
        migrations.CreateModel(
            name='JoinedDeposits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateField(auto_now=True)),
                ('save_trm', models.IntegerField()),
                ('save_amount', models.IntegerField()),
                ('expired_date', models.DateField()),
                ('final_intr_rate', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined_product', to='deposits.depositproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositSpecialCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('거래 연동', '거래 연동'), ('사용 실적', '사용 실적'), ('신규 가입', '신규 가입'), ('비대면/모바일 뱅킹', '비대면/모바일 뱅킹'), ('마케팅 및 기타 동의', '마케팅 및 기타 동의'), ('기타', '기타')], max_length=20)),
                ('condition_content', models.TextField()),
                ('prime_rate', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deposits.depositproducts')),
            ],
        ),
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField()),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='deposits.depositproducts')),
            ],
        ),
    ]
