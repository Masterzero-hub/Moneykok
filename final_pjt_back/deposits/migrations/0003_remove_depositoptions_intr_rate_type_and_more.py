# Generated by Django 4.2.16 on 2024-11-21 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0002_remove_depositoptions_fin_prdt_cd_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositoptions',
            name='intr_rate_type',
        ),
        migrations.RemoveField(
            model_name='depositproducts',
            name='fin_co_no',
        ),
    ]
