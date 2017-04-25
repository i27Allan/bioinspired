from queens.api.chessboard import Chessboard, crossover
from queens.api.charts import line_chart
import random
import copy


class Population(list):
    def __init__(self, population_size, n_queens: int = 8, repr_optimization=False, survivor_selection='fitness_based'):
        super(Population, self).__init__()
        self.population_size = population_size
        self.survivor_selection = 'f' if survivor_selection == 'fitness_based' else 'a'
        self.mean = 0
        for i in range(self.population_size):
            individual = Chessboard(n_queens=n_queens, repr_optimization=repr_optimization)
            self.insort(individual)

    def insort(self, ind: Chessboard):
        l, r = 0, self.__len__()
        while l < r:
            mid = int((l + r) / 2)
            if self.survivor_selection == 'f':
                if ind.fitness > self[mid].fitness:
                    l = mid + 1
                else:
                    r = mid
            else:
                if ind.age > self[mid].age:
                    l = mid + 1
                else:
                    r = mid
        self.insert(l, ind)
        self.evaluate_mean()

    def tournament(self):
        _5selected = list([])
        for i in range(5):
            idx = random.randint(0, self.__len__() - 1)
            _5selected.append(self[idx])
        _5selected = sorted(_5selected, key=lambda ind: ind.fitness)
        _2better = _5selected[-2:]
        c1, c2 = crossover(_2better[0], _2better[1])
        self.offspring_insertion(c1, c2)

    def roulette(self):
        def rotate(population):
            total_fitness = sum(ind.fitness for ind in population)
            picked = random.uniform(0, abs(total_fitness))
            current = 0
            for ind in population:
                current += abs(ind.fitness)
                if current > picked:
                    return ind
            # return population[0]

        parent1, parent2 = rotate(self), rotate(self)
        c1, c2 = crossover(parent1, parent2)
        self.offspring_insertion(c1, c2)

    def offspring_insertion(self, c1: Chessboard, c2: Chessboard):
        if self.survivor_selection == 'f':
            if c1.fitness > c2.fitness:
                c1, c2 = c2, c1
            if c1.fitness >= self[0].fitness:
                self.pop_front()
                self.insort(c1)
            if c2.fitness >= self[0].fitness:
                self.pop_front()
                self.insort(c2)
        else:
            del self[-1]
            del self[-1]
            self.insort(c1)
            self.insort(c2)

    def mutate(self):
        ind = random.randint(0, self.__len__() - 1)
        self[ind].mutate()
        self.evaluate_mean()

    def pop_front(self):
        del self[0]

    def evaluate_mean(self):
        self.mean = sum(ind.fitness for ind in self)/float(self.__len__())

    def increment_age(self):
        for i in self:
            i.age += 1


def solve(n_queens, population_size, repr_optimization, rec_prob: float, mut_prob: float, max_fits: int,
          parent_selection: str = 'tournament', survivor_selection: str = 'fitness_based'):

    population = Population(population_size, n_queens=n_queens, repr_optimization=repr_optimization,
                            survivor_selection=survivor_selection)

    iterations = 0
    gens_mean, gens_higher = [population.mean], [population[-1].fitness]

    pselection = getattr(population, parent_selection)

    best_ind, best_fitness = copy.deepcopy(population[-1]), population[-1].fitness
    while population[-1].fitness < 0 and iterations < max_fits:
        p = random.uniform(0, 1)
        if p <= rec_prob:
            pselection()
        if p <= mut_prob:
            population.mutate()
        iterations += 1
        if population.survivor_selection == 'a':
            population.increment_age()

        if best_fitness < population[-1].fitness:
            best_ind = copy.deepcopy(population[-1])
            best_fitness = population[-1].fitness

        gens_mean.append(population.mean)
        gens_higher.append(population[-1].fitness)

    mean_plot, high_plot = line_chart(gens_mean, gens_higher)
    return {
        'candidate_solution': best_ind,
        'iterations': iterations,
        'mean_plot': mean_plot,
        'high_plot': high_plot
    }



if __name__ == '__main__':
    solve(8, 1000, True, 0.9, 0.4, 10000)