# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 17:03
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='trip',
            managers=[
                ('tManager', django.db.models.manager.Manager()),
            ],
        ),
    ]
