# Generated by Django 3.2.6 on 2021-08-11 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domestic', '0005_auto_20210811_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='dquestion',
            name='home_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic'),
        ),
    ]