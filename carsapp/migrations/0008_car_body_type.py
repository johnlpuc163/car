# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-30 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsapp', '0007_auto_20160619_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='body_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
