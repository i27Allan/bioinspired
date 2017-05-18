from ackley.api.ackley import *
from ackley.api.charts import line_chart, scatter_chart
import numpy as np
import math


class Population(list):
    def __init__(self, population_size: int = 30, dimension: int = 30, lower_bound: float = -15,
                 upper_bound: float = 15,
                 crossover_operator: str = 'intermediary_crossover', global_crossover: bool = True, sigma: float = 0.5,
                 mutation_operator: str = 'gaussian_perturbation', sd_change: str = 'success_rule',
                 from_list=None):
        super(Population, self).__init__()
        self.mean = 0
        self.population_size = population_size
        self.crossover_operator = crossover_operator
        self.global_crossover = global_crossover
        self.sigma = sigma
        self.mutation_operator = mutation_operator
        self.sd_change = sd_change
        if from_list:
            self.extend(from_list[:population_size])
        else:
            PI = 2 * math.acos(-1)
            for i in range(self.population_size):
                individual = Ackley(dimension, ackley_function, 20, 0.2, 2 * PI, lower_bound=lower_bound,
                                    upper_bound=upper_bound)
                self.insort(individual)
        self.evaluate_mean()

    def insort(self, ind: Ackley):
        if self.__len__() == self.population_size and ind.fitness > self[-1].fitness:
            return
        if self.__len__() > 0 and ind.fitness <= self[-1].fitness:
            if self.__len__() < self.population_size:
                self.insert(-1, ind)
            else:
                self[-1] = ind
            self.evaluate_mean()
            return
        l, r = 0, min(self.__len__() - 1, self.population_size - 1)
        while l < r:
            mid = int((l + r) / 2)
            if ind.fitness < self[mid].fitness:
                r = mid
            else:
                l = mid + 1
        if self.__len__() < self.population_size:
            self.insert(l, ind)
        elif self[l].fitness >= ind.fitness:
            self[l] = ind
        self.evaluate_mean()

    def mutate(self):
        if self.__len__() <= 1: return
        ind = np.random.randint(0, self.__len__() - 1)
        self[ind].mutate(self.mutation_operator, self.sd_change)
        tmp = self[ind]
        del self[ind]
        self.insort(tmp)
        self.evaluate_mean()

    def crossover(self):
        child = Ackley.crossover(self, self.crossover_operator, self.global_crossover, self.sigma)
        return child

    def evaluate_mean(self):
        self.mean = sum(ind.fitness for ind in self) / float(self.__len__())


def process(dimensions, mi, lamb, crossover_operator, mutation_operator, standard_deviation_change,
            stop_iterations: bool = True, quantity: int = 100, global_crossover: bool = False,
            mi_plus_lambda: bool = False, sigma: bool = 0.5):
    pop = Population(population_size=mi, dimension=dimensions, crossover_operator=crossover_operator,
                     global_crossover=global_crossover, mutation_operator=mutation_operator, sigma=sigma,
                     sd_change=standard_deviation_change)
    child_pop = Population(population_size=mi, dimension=dimensions, crossover_operator=crossover_operator,
                           global_crossover=global_crossover, mutation_operator=mutation_operator, sigma=sigma,
                           sd_change=standard_deviation_change)
    minimal, before = pop[0], pop[0]
    minimal.fitness += 1e7
    stop_cond, iterations = 0, 0
    fitnesses, means, sum_sd = list([]), list([]), list([])
    while stop_cond < quantity:
        child_pop.clear()
        curr_sd_sum = np.sum(pop[0].standard_deviation)
        print(pop[0].fitness, stop_cond, curr_sd_sum)
        for num_offspring in range(lamb):
            child = pop.crossover()
            if mi_plus_lambda:
                pop.insort(child)
                pop.mutate()
            else:
                child_pop.insort(child)
                child_pop.mutate()
        if not mi_plus_lambda:
            pop = Population(population_size=mi, dimension=dimensions, crossover_operator=crossover_operator,
                             global_crossover=global_crossover, mutation_operator=mutation_operator, sigma=sigma,
                             sd_change=standard_deviation_change, from_list=child_pop)
        minimal = pop[0] if pop[0].fitness < minimal.fitness else minimal
        fitnesses.append(pop[0].fitness)
        sum_sd.append(np.sum(pop[0].standard_deviation))
        means.append(pop.mean)
        if stop_iterations:
            stop_cond += 1
        else:
            if pop[0].fitness == before.fitness: stop_cond += 1
            else: stop_cond = 0
        before = pop[0]
        iterations += 1
    mean_plot = line_chart(means, 'Mean', '# generation', 'fitness')
    high_plot = line_chart(fitnesses, 'Lowest', '# generation', 'fitness')
    sum_sd_plot = line_chart(sum_sd, 'SD sum', '# generation', '# SD sum')
    return {
        'candidate_solution': minimal,
        'iterations': iterations,
        'mean_plot': mean_plot,
        'high_plot': high_plot,
        'high_scatter': scatter_chart(means, fitnesses),
        'sum_sd_plot': sum_sd_plot
    }


if __name__ == '__main__':
    process(100, 300, mi_plus_lambda=False)
