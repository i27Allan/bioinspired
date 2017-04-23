import numpy as np
from bitstring import BitArray
import random


class Chessboard(list):
    def __init__(self, n_queens: int = 8, from_list=None, from_bits: str = '', repr_optimization=False):
        """
        :param n_queens: number of queens at chessboard
        :param repr_optimization: False implies bit string representation will be used
        randomly generate the genotype and compute its fitness
        """
        # if from_list is None:
        #     from_list = []
        self.repr_optimization = repr_optimization
        if from_list:
            self.length = len(from_list)
            super(Chessboard, self).__init__()
            self.extend(from_list)
        else:
            self.length = n_queens
            super(Chessboard, self).__init__()
            self.extend(self.__genotype__())
        self.fitness = None
        self.evaluate_fitness()

    def __genotype__(self):
        """
        generate the genotype randomly. 
        if optimization is True, cases of two or more chromosomes 
        standing at same row are avoided
        :return: rep, genotype with n_queens chromosomes 
        """
        rep = list([])
        taken = [False]*self.length
        while len(rep) < self.length:
            ch = random.randint(0, self.length - 1)
            if self.repr_optimization and taken[ch]:
                continue
            rep.append(ch)
            taken[ch] = True
        return rep

    def evaluate_fitness(self):
        # columns clashes
        clashes = 0 if self.repr_optimization else abs(self.length - len(np.unique(self)))
        # diagonal clashes
        for i in range(self.length):
            for j in range(i+1, self.length):
                if j-i == abs(self[i] - self[j]):
                    clashes += 1
        # fitness is the opposite value of clashes
        # therefore the fitness is inversely proportional to number of clashes
        self.fitness = -clashes

    def mutate(self):
        pos1 = random.randint(0, self.length - 1)  # position to be mutated

        def bit_flip(self):
            # mutation at bit string chromosome
            shift = random.randint(0, int(self.length - 1).bit_length())
            if self[pos1] & (1 << shift):
                self[pos1] &= ~(1 << shift)
            else:
                self[pos1] |= (1 << shift)

        def swap(self):
            pos2 = random.randint(0, self.length - 1)
            while pos2 == pos1:
                pos2 = random.randint(0, self.length - 1)  # position to be swapped with pos1
            self[pos1], self[pos2] = self[pos2], self[pos1]

        if not self.repr_optimization:
            bit_flip(self)
        else:
            swap(self)

        self.evaluate_fitness()  # re-evaluate fitness

    def __to_bits__(self):
        bits = ''
        for n in self:
            bits += BitArray(uint=n, length=3).bin
        return bits

    def __str__(self):
        if self.repr_optimization:
            return super(Chessboard, self).__str__()
        else:
            return self.__to_bits__()


def crossover(gen1: Chessboard, gen2: Chessboard):
    class CrossoverNotSupportedException(Exception):
        pass

    length = len(gen1)
    if length != len(gen2):
        raise CrossoverNotSupportedException('Genotypes have different lengths')

    repr_optimization = gen1.repr_optimization or gen2.repr_optimization

    def __one_point__(gen1, gen2):
        c1, c2 = [], []
        if repr_optimization:
            point = random.randint(0, length - 1)
            c1 = gen1[:point]
            c2 = gen2[:point]
            print([i for i in range(point, length)])
            for i in range(point, length):
                if gen2[i] not in c1:
                    c1.append(gen2[i])
                if gen1[i] not in c2:
                    c2.append(gen1[i])
            for i in range(point, length):
                len1, len2 = len(c1), len(c2)
                if len1 == length and len2 == length:
                    break
                if len1 < length and gen1[i] not in c1:
                    c1.append(gen1[i])
                if len2 < length and gen2[i] not in c2:
                    c2.append(gen2[i])
        else:
            point = random.randint(0, 3*length-1)
            print(point)
            block, offset = int(point/3), point % 3
            if offset == 0:
                c1 = gen1[:block] + gen2[block:]
                c2 = gen2[:block] + gen1[block:]
            else:
                next_block = block+1
                n1 = gen1[next_block] & (1 << (3-offset))
                n2 = gen2[next_block] & ~(1 << (3-offset))
                n_res = n1+n2
                c1 = gen1[:block] + [n_res] + gen2[next_block:]

                n1 = gen2[next_block] & (1 << (3 - offset))
                n2 = gen1[next_block] & ~(1 << (3 - offset))
                n_res = n1 + n2
                c2 = gen2[:block] + [n_res] + gen1[next_block:]

        return c1, c2

        # print('POINT', point)
        # child1 = list(set(gen1[:point] + gen2[point:] + gen1[point:]))
        # child2 = list(set(gen2[:point] + gen1[point:] + gen2[point:]))
        # return child1, child2

    child1, child2 = __one_point__(gen1, gen2)
    return Chessboard(from_list=child1, repr_optimization=repr_optimization), Chessboard(from_list=child2, repr_optimization=repr_optimization)


if __name__ == '__main__':
    # unit test
    p1 = Chessboard(repr_optimization=False)
    p2 = Chessboard(repr_optimization=False)
    print('PARENT1', p1, p1.fitness)
    print('PARENT2', p2, p2.fitness)
    c1, c2 = crossover(p1, p2)
    print(c1, c1.fitness)
    print(c2, c2.fitness)

    # print(c)


