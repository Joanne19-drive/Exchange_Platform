# Generated by Django 3.2.6 on 2021-08-09 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0002_initial'),
        ('domestic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foreign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dquestion',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dquestion',
            name='away_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foreign.foreign'),
        ),
        migrations.AddField(
            model_name='dquestion',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.country'),
        ),
        migrations.AddField(
            model_name='dquestion',
            name='home_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic'),
        ),
        migrations.AddField(
            model_name='domestic',
            name='home_sister',
            field=models.ManyToManyField(related_name='sisters', to='foreign.Foreign', verbose_name='자매결연'),
        ),
        migrations.AddField(
            model_name='dcomment',
            name='comment_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dcomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domestic.dquestion'),
        ),
        migrations.AddField(
            model_name='credit',
            name='away_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foreign.foreign'),
        ),
        migrations.AddField(
            model_name='credit',
            name='credit_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='credit',
            name='home_school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic'),
        ),
    ]
