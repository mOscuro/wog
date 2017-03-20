# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-15 16:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workout', '0001_initial'),
        ('round', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wod_step', to='workout.Workout'),
        ),
        migrations.AddField(
            model_name='round',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='workout.Workout'),
        ),
    ]
