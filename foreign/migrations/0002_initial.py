# Generated by Django 3.2.6 on 2021-08-06 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foreign', '0001_initial'),
        ('country', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('domestic', '0002_domestic_home_sister'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fquestion',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fquestion',
            name='away_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foreign.foreign'),
        ),
        migrations.AddField(
            model_name='fquestion',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.country'),
        ),
        migrations.AddField(
            model_name='fquestion',
            name='home_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic'),
        ),
        migrations.AddField(
            model_name='foreign',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_univs', to='country.country'),
        ),
        migrations.AddField(
            model_name='fcomment',
            name='comment_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fcomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign.fquestion'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='foreign.post'),
        ),
    ]
