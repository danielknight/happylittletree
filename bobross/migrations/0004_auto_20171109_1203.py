# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-09 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobross', '0003_auto_20171108_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userart',
            name='painting',
            field=models.ImageField(default='bobross/media/default.png', upload_to='bobross/media/user_paintings'),
        ),
    ]
