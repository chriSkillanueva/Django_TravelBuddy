# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_auto_20161021_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='user_id',
            new_name='user',
        ),
    ]
