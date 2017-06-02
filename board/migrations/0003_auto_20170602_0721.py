# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-01 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20170602_0710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posting',
            options={'ordering': ['-create_date']},
        ),
        migrations.AlterField(
            model_name='posting',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='posting',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
