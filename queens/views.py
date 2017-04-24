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
            plots_title = hashlib.md5(str(time.time()).encode('utf')).hexdigest() + '.png'
            ret = solver.solve(
                n_queens=data['number_of_queens'],
                population_size=data['population_size'],
                repr_optimization=(data['representation'] != 'bitstring'),
                rec_prob=data['probability_of_crossover'],
                mut_prob=data['probability_of_mutation'],
                max_fits=data['max_fitness_evaluations'],
                out_file='static/charts/mean_high_plot/{}'.format(plots_title),
            )
            context['candidate_solution'] = ret.get('candidate_solution')
            context['iterations'] = ret.get('iterations')
            context['plots_title'] = plots_title

        return render(request, 'index.html', context)

