# Generated by Django 3.2.6 on 2021-11-07 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foreign', '0010_alter_foreign_away_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fquestion',
            name='hits',
            field=models.PositiveIntegerField(default=0, verbose_name='조회수'),
        ),
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.PositiveIntegerField(default=0, verbose_name='조회수'),
        ),
    ]
