from django.shortcuts import render
from django.views import View
from nqueens.forms import *
from nqueens.api import solver
import time
import hashlib


# Create your views here.
class IndexView(View):
    form = GeneticOptionsForm

    def get(self, request):
        form = self.form()
        return render(request, 'queens/index.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            options = form.save(commit=False)
            ret = solver.solve(
                n_queens=options.number_of_queens,
                population_size=options.population_size,
                repr_optimization=(options.representation != 'bitstring'),
                rec_prob=options.probability_of_crossover,
                mut_prob=options.probability_of_mutation,
                max_fits=options.max_fitness_evaluations,
                parent_selection=options.parent_selection,
                survivor_selection=options.survivor_selection,
            )
            context['candidate_solution'] = ret.get('candidate_solution')
            context['iterations'] = ret.get('iterations')
            context['mean_plot'] = ret.get('mean_plot')
            context['high_plot'] = ret.get('high_plot')
            context['n_queens'] = range(int(options.number_of_queens))

        return render(request, 'queens/index.html', context)


def index(request):
    return render(request, 'index.html', locals())