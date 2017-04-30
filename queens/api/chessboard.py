import numpy as np
from bitstring import BitArray
import random


class Chessboard(list):
    def __init__(self, n_queens: int = 8, from_list=None, repr_optimization=False):
        """
        :param n_queens: number of queens at chessboard
        :param from_list: to initialize the chessboard genotype from a existing list 
        :param repr_optimization: False implies bit string representation will be used
        randomly generate the genotype and compute its fitness
        """
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
        self.age = 0
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
                self[pos1] = (self[pos1] & ~(1 << shift)) % self.length
            else:
                self[pos1] = (self[pos1] | (1 << shift)) % self.length

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
        # print the genotype in a bit string format
        bits = ''
        for n in self:
            bits += BitArray(uint=n, length=int(self.length).bit_length()).bin + ' '
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
        print(gen1)
        print(gen2)
        raise CrossoverNotSupportedException('Genotypes have different lengths')

    repr_optimization = gen1.repr_optimization or gen2.repr_optimization

    def __one_point__(gen1, gen2):
        c1, c2 = [], []
        if repr_optimization:
            """
            if the representation is through integers, the crossover process
            is applied slicing the left part of gen1 and the right part of gen2 to
            be the child1 and the left part of gen2 and the right part of gen1 to
            be the child2.
            """
            point = random.randint(0, length - 1)
            c1 = gen1[:point]
            c2 = gen2[:point]
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
            """
            if the representation is through bit string, the crossover process is
            similar to the related above, but with one difference: the point-of-slice
            is now calculated considering the whole bits of the representation.
            If the point-of-slice falls on the 'middle' of a number, bitwise operations
            are performed with aim to slice this number.
            
            e.g:
                PARENT1 001 001 100 110 110 000 100 011  
                PARENT2 000 010 100 101 010 110 111 101
                
                POINT-OF-SLICE: 16
                
                falls on the 0-1st bit of 5th block of n-bits (with 0-indexed positions).
                Therefore, the slicing will be this way:
                
                CHILD1: 001 001 100 110 0\\10 110 111 101 (left of '\\' is from PARENT1 and the right is from PARENT2)
                CHILD2: 000 010 100 101 1\\00 000 100 011 (left of '\\' is from PARENT2 and the right is from PARENT1)
            """
            global c1, c2
            point = random.randint(0, 3*length-1)  # gets the point-of-slice
            block, offset = int(point/3), point % 3  # figures out which block of n-bits the slicing will occur
            block = max(0, block-1)  # adjusts to 0-indexed
            if offset == 0:
                # if the point fell on division of two blocks, just concatenate the arrays
                c1 = gen1[:block] + gen2[block:]
                c2 = gen2[:block] + gen1[block:]
            else:
                # if the point fell in a middle of an block, the slice will divide this number's bits
                next_block = 0 if block == 0 else block+1  # the next is where the offset is positioned
                # print("OIII", block, next_block, point, length)
                bit_size = int(length - 1).bit_length()  # gets the size of each block
                shift_size = bit_size - offset

                n1 = (gen1[next_block] >> shift_size) << shift_size  # gets the 'shift_size' first bits of parent1
                n2 = gen2[next_block] & ((1 << shift_size) - 1)  # gets the 'shift_size' last bits of parent2
                n_res = n1 | n2  # concatenate them
                adder = next_block + (next_block == 0)
                c1 = gen1[:block] + [n_res] + gen2[adder:]  # builds the child1

                n1 = (gen2[next_block] >> shift_size) << shift_size  # gets the 'shift_size' first bits of parent2
                n2 = gen1[next_block] & ((1 << shift_size) - 1)  # gets the 'shift_size' last bits of parent1
                n_res = n1 | n2  # concatenate them
                adder = next_block + (next_block == 0)
                c2 = gen2[:block] + [n_res] + gen1[adder:]  # builds the child2
        return c1, c2

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


