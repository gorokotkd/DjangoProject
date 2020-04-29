# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-29 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_opcion_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.CharField(default='No topic', max_length=200),
        ),
    ]
