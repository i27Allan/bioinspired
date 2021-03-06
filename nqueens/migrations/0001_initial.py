# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneticOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_queens', models.IntegerField()),
                ('population_size', models.IntegerField()),
                ('representation', models.CharField(choices=[('bitstring', 'Bit String'), ('numbered', 'Integers')], max_length=50)),
                ('probability_of_crossover', models.FloatField()),
                ('probability_of_mutation', models.FloatField()),
                ('parent_selection', models.CharField(choices=[('tournament', 'Tournament'), ('roulette', 'Roulette Wheel')], max_length=50)),
                ('survivor_selection', models.CharField(choices=[('age_based', 'Age Based Selection'), ('fitness_based', 'Fitness Based Selection')], max_length=50)),
                ('max_fitness_evaluations', models.IntegerField()),
            ],
        ),
    ]
