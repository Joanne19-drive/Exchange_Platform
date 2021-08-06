# Generated by Django 3.2.6 on 2021-08-06 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foreign', '0001_initial'),
        ('domestic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='domestic',
            name='home_sister',
            field=models.ManyToManyField(related_name='sisters', to='foreign.Foreign', verbose_name='자매결연'),
        ),
    ]
