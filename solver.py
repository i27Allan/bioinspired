from chessboard import Chessboard, crossover
import random


class Population(list):
    def __init__(self):
        super(Population, self).__init__()

    def insort(self, ind: Chessboard):
        l, r = 0, self.__len__()
        while l < r:
            mid = int((l + r) / 2)
            if ind.fitness > self[mid].fitness:
                l = mid + 1
            else:
                r = mid
        self.insert(l, ind)

    def better2of5(self):
        _5selected = list([])
        for i in range(5):
            idx = random.randint(0, self.__len__() - 1)
            _5selected.append(self[idx])
        _5selected = sorted(_5selected, key=lambda ind: ind.fitness)
        _2better = _5selected[-2:]
        return crossover(_2better[0], _2better[1])

    def mutate(self):
        ind = random.randint(0, self.__len__() - 1)
        self[ind].mutate()


def solve(population_size, repr_optimization, rec_prob: float, mut_prob: float):
    population = Population()

    for i in range(population_size):
        individual = Chessboard(repr_optimization=repr_optimization)
        population.insort(individual)

    iterations = 0
    while population[-1].fitness < 0 and iterations < 10000:
        p = random.uniform(0, 1)
        if p <= rec_prob:
            c1, c2 = population.better2of5()
            if c1.fitness > c2.fitness:
                c1, c2 = c2, c1
            if c1.fitness > population[0].fitness:
                del population[0]
                population.insort(c1)
            if c2.fitness > population[0].fitness:
                del population[0]
                population.insort(c2)
        if p <= mut_prob:
            population.mutate()
        iterations += 1

    print(population[-1], iterations)

if __name__ == '__main__':
    solve(100, True, 0.9, 0.4)
