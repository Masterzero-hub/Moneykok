# Generated by Django 4.2.4 on 2024-11-26 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.CharField(max_length=100)),
                ('cur_nm', models.CharField(max_length=100)),
                ('ttb', models.CharField(max_length=100)),
                ('tts', models.CharField(max_length=100)),
                ('deal_bas_r', models.CharField(max_length=100)),
            ],
        ),
    ]
