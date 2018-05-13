import csv
from evidence import Evidence
import random
from gaussian import Gaussian

def generate_evidence():
    evidence = []

    with open('datasets/perfume_data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            for measurement in row[1:]:
                evidence.append(Evidence(float(measurement.replace(",", "."))))
    
    return evidence

def generate_initial_gaussians(amount, minvalue, maxvalue):
    gaussians = []
    for i in range(amount):
        gaussians.append(Gaussian(random.gauss((maxvalue-minvalue)/2, 10), max(1, random.gauss(3, 3)), 1.0/amount))
    return gaussians
