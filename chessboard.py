import numpy as np
import random


class Chessboard(list):
    def __init__(self, n_queens: int = 8, optimization=False):
        """
        :param n_queens: number of queens at chessboard
        :param optimization: False implies bit string representation will be used
        randomly generate the genotype and compute its fitness
        """
        self.length = n_queens
        super(Chessboard, self).__init__()
        self.optimization = optimization
        self.extend(self.__genotype__())
        self._fitness = None
        self.fitness()


    def __genotype__(self):
        """
        generate the genotype randomly. 
        if optimization is True, cases of two or more chromosomes 
        standing at same row are avoided
        :return: rep, genotype with n_queens chromosomes 
        """
        rep = list() if not self.optimization else set({})
        while len(rep) < self.length:
            ch = random.randint(0, self.length - 1)
            rep = rep.append(ch) if not self.optimization else rep | {ch}
        return rep

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self):
        # columns clashes
        clashes = 0 if self.optimization else abs(self.length - len(np.unique(self)))
        # diagonal clashes
        for i in range(self.length):
            for j in range(self.length):
                if i != j and abs(i-j) == abs(self[i] - self[j]):
                    clashes += 1
        # fitness is the opposite value of clashes
        # therefore the fitness is inversely proportional to number of clashes
        self._fitness = -clashes

    def mutate(self):
        pos1 = random.randint(0, self.length - 1) # position to be mutated
        if not self.optimization:
            # mutation at bit string chromosome
            shift = random.randint(0, int(self.length-1).bit_length())
            if self[pos1] & (1 << shift):
                self[pos1] &= ~(1 << shift)
            else:
                self[pos1] |= (1 << shift)
        else:
            pos2 = pos1
            while pos2 == pos1:
                pos2 = random.randint(0, self.length - 1) # position to be swapped with pos1
            self[pos1], self[pos2] = self[pos2], self[pos1]

        self.fitness() # re-evaluate fitness




