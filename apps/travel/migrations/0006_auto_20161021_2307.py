# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 23:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_auto_20161021_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='join',
            old_name='trip',
            new_name='trip_id',
        ),
        migrations.RenameField(
            model_name='join',
            old_name='user',
            new_name='user_id',
        ),
    ]