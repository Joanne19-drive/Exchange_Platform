# Generated by Django 3.2.6 on 2021-08-09 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Foreign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('away_name', models.CharField(max_length=50)),
                ('away_apply', models.TextField(blank=True)),
                ('language_score', models.TextField(blank=True)),
                ('course_enroll', models.TextField(blank=True)),
                ('accommodation', models.TextField(blank=True)),
                ('atmosphere', models.TextField(blank=True)),
                ('club', models.TextField(blank=True)),
                ('away_scholarship', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=50)),
                ('question_content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('away_year', models.IntegerField()),
                ('away_semester', models.CharField(choices=[('1', '1'), ('2', '2')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('foreign', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='foreign.foreign')),
            ],
        ),
    ]
