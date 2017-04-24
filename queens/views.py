from django.shortcuts import render
from django.views import View
from queens.forms import *
from queens.api import solver
import time
import hashlib

# Create your views here.
class IndexView(View):
    form = OptionsForm

    def get(self, request):
        form = self.form()
        return render(request, 'index.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            data = form.cleaned_data
            ret = solver.solve(
                n_queens=data['number_of_queens'],
                population_size=data['population_size'],
                repr_optimization=(data['representation'] != 'bitstring'),
                rec_prob=data['probability_of_crossover'],
                mut_prob=data['probability_of_mutation'],
                max_fits=data['max_fitness_evaluations'],
                to_django=True,
            )
            context['candidate_solution'] = ret.get('candidate_solution')
            context['iterations'] = ret.get('iterations')
            context['mean_high_plot'] = ret.get('mean_high_plot')
            context['n_queens'] = range(int(data['number_of_queens']))

        print(context)
        return render(request, 'index.html', context)

