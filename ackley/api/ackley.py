import numpy as np


def ackley_function(params: np.array, *args):
    args = args[0]
    c1, c2, c3 = args[0], args[1], args[2]
    _N = len(params)
    sum_xi2 = np.sum(np.square(params))
    sum_cos_c3xi = np.sum(np.cos(np.multiply(params, c3)))
    f_x = -c1 * np.exp(-c2 * np.sqrt((1 / _N) * sum_xi2)) - np.exp((1 / _N) * sum_cos_c3xi) + c1 + np.exp(1)
    return f_x


class Ackley(object):
    def __init__(self, dimension: int, fitness_function, *args, lower_bound:float =0,
                 upper_bound:float =0, genotype=None, standard_deviation=None):
        """
        :param dimension: number of nqueens at chessboard
        :param genotype: to initialize the chessboard genotype from a existing list
        :param float_genotype: True if it the genotype will have float values
        """
        self.fitness_function = fitness_function
        self.fitness_function_args = args[0] if isinstance(args[0], tuple) else args
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mutations, self.successful_mutations = 0, 0

        self.genotype = np.array(genotype) if genotype else self.__genotype__()
        self.standard_deviation = np.array(standard_deviation) if standard_deviation else self.__standard_deviation__()
        self.fitness = None
        self.evaluate_fitness()

    def __lt__(self, other):
        if isinstance(other, Ackley):
            return self.fitness < other.fitness
        return self.fitness < other

    def __genotype__(self):
        return np.random.uniform(low=self.lower_bound, high=self.upper_bound, size=(self.dimension,))

    def __standard_deviation__(self):
        var = np.sqrt(np.var(self.genotype))
        return np.random.uniform(low=0, high=var, size=(self.dimension,))

    def evaluate_fitness(self):
        self.fitness = self.fitness_function(self.genotype, self.fitness_function_args)

    def change_standard_deviation(self, kind_of_heuristic):

        def success_rate():
            success_rate = float(self.successful_mutations) / self.mutations
            c = np.random.uniform(low=0.8, high=1.0)
            sd = None
            if success_rate > 0.2:
                sd = (1 / c) * self.standard_deviation
            elif success_rate < 0.2:
                sd = c * self.standard_deviation
            else:
                sd = self.standard_deviation
            sd[sd < 1e-4] = 1e-4
            return sd

        def gaussian_multiple():
            gaussian_dsd = np.random.normal(0, self.standard_deviation, self.dimension)
            sd = np.array(self.standard_deviation*np.exp(gaussian_dsd))
            sd[sd < 1e-4] = 1e-4
            return sd

        new_sd = locals()[kind_of_heuristic]
        self.standard_deviation = np.nan_to_num(new_sd())

    def mutate(self, kind_of_mutation, kind_of_change_sd):

        def gaussian_perturbation():
            # print(self.genotype)
            candidate_genotype = np.array(self.genotype + np.random.normal(0, self.standard_deviation, self.dimension))
            candidate_genotype[candidate_genotype > 15] = np.random.uniform(low=-15, high=15)
            candidate_genotype[candidate_genotype < 15] = np.random.uniform(low=-15, high=15)
            candidate_fitness = self.fitness_function(candidate_genotype, self.fitness_function_args)
            if candidate_fitness < self.fitness:
                self.genotype = candidate_genotype
                self.fitness = candidate_fitness
                self.successful_mutations += 1.0

        self.mutations += 1.0
        self.change_standard_deviation(kind_of_change_sd)
        mutation_func = locals()[kind_of_mutation]
        mutation_func()

    @staticmethod
    def crossover(population, kind_of_crossover: str, global_crossover: bool = False, sigma: float = 0.5):

        def uniform_crossover(p1, p2, index, **kwargs):
            _X = np.random.uniform(low=0, high=1.0)
            gen = p1.genotype[index] if _X <= 0.5 else p2.genotype[index]
            sd = p1.standard_deviation[index] if _X <= 0.5 else p2.standard_deviation[index]
            return gen, sd

        def intermediary_crossover(p1, p2, index, **kwargs) -> (Ackley, Ackley):
            s = kwargs.pop('sigma')
            sd = (1 - s) * p1.standard_deviation[index] + s * p2.standard_deviation[index]
            gen = (1 - s) * p1.genotype[index] + s * p2.genotype[index]
            return gen, sd

        individual = population[-1]
        genotype_len = len(individual.genotype)
        population_len = len(population)
        crossover_func = locals()[kind_of_crossover]
        child_genotype = list([0] * genotype_len)
        child_sd = list([0] * genotype_len)
        i, j = np.random.randint(low=0, high=population_len), np.random.randint(low=0, high=population_len)
        for idx in range(genotype_len):
            if global_crossover:
                i, j = np.random.randint(low=0, high=population_len), np.random.randint(low=0, high=population_len)
            child_genotype[idx], child_sd[idx] = crossover_func(population[i], population[j], idx, sigma=sigma)

        child = Ackley(individual.dimension, individual.fitness_function, individual.fitness_function_args,
                       genotype=child_genotype, lower_bound=individual.lower_bound, upper_bound=individual.upper_bound,
                       standard_deviation=child_sd)

        return child

if __name__ == '__main__':
    import math
    PI = math.acos(-1)
    population = list([])
    for i in range(30):
        population.append(Ackley(30, ackley_function, 20, 0.2, 2*PI, lower_bound=-15, upper_bound=15))

    fitness = [p.fitness for p in population]
    print(min(fitness))
