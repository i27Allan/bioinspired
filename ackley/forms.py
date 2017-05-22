from django import forms
from ackley.models import *


class EvolutionaryOptionsForm(forms.ModelForm):
    class Meta:
        model = EvolutionaryOptions
        fields = '__all__'

        widgets = {
            'number_of_dimensions': forms.NumberInput(attrs={'min': 1, 'max': 40}),
            'mi_size': forms.NumberInput(attrs={'min': 1, 'max': 200}),
            'lambda_size': forms.NumberInput(attrs={'min': 1, 'max': 200}),
            'delta': forms.NumberInput(attrs={'min': 0, 'max': 1}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 1000})
        }
