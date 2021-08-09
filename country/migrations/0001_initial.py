# Generated by Django 3.2.6 on 2021-08-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=50, verbose_name='나라 이름')),
                ('visa', models.TextField(blank=True, verbose_name='비자 발급 방법')),
                ('lifestyle', models.TextField(blank=True, verbose_name='현지 생활 및 치안')),
                ('money', models.TextField(blank=True, verbose_name='물가 및 체류 비용')),
                ('culture', models.TextField(blank=True, verbose_name='문화적 특징')),
                ('covid_info', models.TextField(blank=True, verbose_name='코로나 정보')),
            ],
        ),
        migrations.CreateModel(
            name='CQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=50)),
                ('question_content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
