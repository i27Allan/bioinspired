# import numpy as np
from bitstring import BitArray
import random


class Chessboard(list):
    def __init__(self, n_queens: int = 8):
        """
        :param n_queens: number of queens at chessboard
        randomly generate the initial population and compute its fitness
        """
        self.length = n_queens
        super(Chessboard, self).__init__()
        self.extend(self.__genotype_bit_str__())
        self.fitness = list([])*n_queens

    def __genotype_bit_str__(self):
        rep = set({})
        bits_len = len(bin(self.length)) - 2
        while len(rep) < self.length:
            gen = random.randint(0, self.length - 1)
            bits = BitArray(uint=gen, length=bits_len)
            rep = rep | {bits.bin}
        return rep

    def __genotype_int_array__(self, n_queens: int):
        pass

    def evaluate_fitness(self):
        pass


