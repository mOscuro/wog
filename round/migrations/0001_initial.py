# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-10 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_repeat', models.IntegerField(default=1)),
                ('position', models.PositiveSmallIntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_rep', models.IntegerField(default=1)),
                ('distance', models.IntegerField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('rest_time', models.IntegerField(default=0)),
                ('position', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_steps', to='round.Round')),
            ],
        ),
    ]
