# Generated by Django 3.2.6 on 2021-08-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_certificate',
            field=models.BooleanField(default=False, verbose_name='학교 인증 여부'),
        ),
    ]