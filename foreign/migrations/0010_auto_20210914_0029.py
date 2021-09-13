# Generated by Django 3.2.6 on 2021-09-13 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foreign', '0009_auto_20210814_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='fcomment',
            name='secret',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='foreign',
            name='away_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
