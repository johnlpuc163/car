# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-19 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsapp', '0005_auto_20160618_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='updated_at',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='created_at',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='updated_at',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
