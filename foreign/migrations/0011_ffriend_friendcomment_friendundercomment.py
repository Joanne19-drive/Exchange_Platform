# Generated by Django 3.2.6 on 2021-10-03 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foreign', '0010_alter_foreign_away_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FFriend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('foreign', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='find_friend', to='foreign.foreign')),
                ('friend_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_friend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('secret', models.BooleanField(default=False)),
                ('comment_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ffriend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign.ffriend')),
            ],
        ),
        migrations.CreateModel(
            name='FriendUnderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(blank=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign.friendcomment')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
