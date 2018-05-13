import numpy as np
import scipy.stats as stats
import itertools

class Gaussian:
    newid = itertools.count().next

    def __init__(self, mean, std, weight):
        self.mean = mean
        self.std = std
        self.weight = weight
        self.id = Gaussian.newid()
    
    def get_density_value(self, evidence):
        return stats.norm.pdf(evidence.value, self.mean, self.std)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "G(" + str(self.id) + ")" # with mean " + str(self.mean) + " and std " + str(self.std)

    def __str__(self):
        return "G(" + str(self.id) + ")" # with mean " + str(self.mean) + " and std " + str(self.std)