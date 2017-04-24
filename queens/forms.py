from django import forms


class OptionsForm(forms.Form):
    number_of_queens = forms.IntegerField(max_value=30, min_value=4)
    population_size = forms.IntegerField(min_value=2)
    representation = forms.ChoiceField(widget=forms.Select(),
                                       choices=[
                                               ('bitstring', 'Bit String'),
                                               ('numbered', 'Integers')
                                                ])
    probability_of_crossover = forms.FloatField(min_value=0, max_value=1.0)
    probability_of_mutation = forms.FloatField(min_value=0, max_value=1.0)
    max_fitness_avaliations = forms.IntegerField(min_value=1)