from django.shortcuts import render
from django.views import View
from ackley.forms import *
from ackley.api.population import process


# Create your views here.
class IndexView(View):
    form = EvolutionaryOptionsForm

    def get(self, request):
        form = self.form()
        return render(request, 'ackley/index.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        context = {'form': form}
        if form.is_valid():
            options = form.save(commit=False)
            crossover_op = 'intermediary_crossover' if options.crossover_operator.endswith('intermediary') else \
                'uniform_crossover'
            ret = process(dimensions=options.number_of_dimensions,
                          mi=options.mi_size,
                          lamb=options.lambda_size,
                          mi_plus_lambda=('plus' in options.survivor_selection),
                          crossover_operator=crossover_op,
                          global_crossover=options.crossover_operator.startswith('global'),
                          sigma=options.sigma,
                          mutation_operator=options.mutation_operator,
                          standard_deviation_change=options.standard_deviation_change,
                          stop_iterations=options.stop_condition.endswith('iterations'),
                          quantity=options.quantity,
                          )
            context['candidate_solution'] = ret.get('candidate_solution')
            context['iterations'] = ret.get('iterations')
            context['mean_plot'] = ret.get('mean_plot')
            context['high_plot'] = ret.get('high_plot')
            context['high_scatter'] = ret.get('high_scatter')
            context['sum_sd_plot'] = ret.get('sum_sd_plot')
        return render(request, 'ackley/index.html', context)
