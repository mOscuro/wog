# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-10 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('level', models.IntegerField(choices=[(1, 'Amateur'), (2, 'Easy'), (3, 'Medium'), (4, 'Hard'), (5, 'Expert')], default=3)),
                ('type', models.IntegerField(choices=[(0, 'Bodyweight'), (1, 'Weightlifting'), (2, 'Powerlifting'), (3, 'TRX')], default=0)),
                ('equipement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exercise.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscles',
            field=models.ManyToManyField(blank=True, to='exercise.Muscle'),
        ),
    ]
