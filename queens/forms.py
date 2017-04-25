from django import forms
from queens.models import *


class GeneticOptionsForm(forms.ModelForm):
    class Meta:
        model = GeneticOptions
        fields = '__all__'

        widgets = {
            'number_of_queens': forms.NumberInput(attrs={'min': 4, 'max': 40}),
            'population_size': forms.NumberInput(attrs={'min': 2}),
            'probability_of_mutation': forms.NumberInput(attrs={'min': 0, 'max': 1}),
            'probability_of_crossover': forms.NumberInput(attrs={'min': 0, 'max': 1}),
            'max_fitness_evaluations': forms.NumberInput(attrs={'min': 1})
        }
