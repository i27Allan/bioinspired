from django.db import models

# Create your models here.
class GeneticOptions(models.Model):
    number_of_queens = models.IntegerField()
    population_size = models.IntegerField()
    representation = models.CharField(max_length=50, choices=[
        ('bitstring', 'Bit String'),
        ('numbered', 'Integers')
    ])
    probability_of_crossover = models.FloatField()
    probability_of_mutation = models.FloatField()
    parent_selection = models.CharField(max_length=50, choices=[
        ('tournament', 'Tournament'),
        ('roulette', 'Roulette Wheel'),
    ])
    survivor_selection = models.CharField(max_length=50, choices=[
        ('age_based', 'Age Based Selection'),
        ('fitness_based', 'Fitness Based Selection')
    ])
    max_fitness_evaluations = models.IntegerField()