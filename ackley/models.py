from django.db import models


# Create your models here.
class EvolutionaryOptions(models.Model):
    number_of_dimensions = models.IntegerField()
    survivor_selection = models.CharField(max_length=50, choices=[
        ('mi_plus_lambda', 'μ + λ'),
        ('mi_comma_lambda', 'μ, λ')
    ])
    mi_size = models.IntegerField()
    lambda_size = models.IntegerField()
    crossover_operator = models.CharField(max_length=50, choices=[
        ('local_intermediary', 'Local Intermediary'),
        ('global_intermediary', 'Global Intermediary'),
        ('local_uniform', 'Local Uniform'),
        ('global_uniform', 'Global Uniform')
    ])
    delta = models.FloatField(blank=True, null=True)
    mutation_operator = models.CharField(max_length=50, choices=[
        ('gaussian_perturbation', 'Gaussian Perturbation'),
    ])
    standard_deviation_change = models.CharField(max_length=50, choices=[
        ('success_rate', 'Success Rate'),
        ('gaussian_multiple', 'Gaussian Multiple')
    ])
    stop_condition = models.CharField(max_length=50, choices=[
        ('number_of_iterations', 'Number of Iterations'),
        ('number_of_draws', 'Number of draws'),
    ])
    quantity = models.IntegerField()

