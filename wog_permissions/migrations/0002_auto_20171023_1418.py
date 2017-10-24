# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-23 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wog_permissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsessionpermissiongroup',
            name='profile_type',
            field=models.IntegerField(choices=[(0, 'guests'), (1, 'spectators'), (3, 'competitors')], default=3),
        ),
    ]