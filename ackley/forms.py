from django import forms
from ackley.models import *


class EvolutionaryOptionsForm(forms.ModelForm):
    class Meta:
        model = EvolutionaryOptions
        fields = '__all__'

        widgets = {
            'number_of_dimensions': forms.NumberInput(attrs={'min': 2, 'max': 40}),
            'mi_size': forms.NumberInput(attrs={'min': 2}),
            'lambda_size': forms.NumberInput(attrs={'min': 4}),
            'sigma': forms.NumberInput(attrs={'min': 0, 'max': 1}),
            'quantity': forms.NumberInput(attrs={'min': 1})
        }
