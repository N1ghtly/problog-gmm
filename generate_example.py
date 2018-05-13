import numpy as np
import random
from itertools import repeat

nr_of_clusters = 8
data_range = 100
nr_of_datapoints = 100
cl_constraints = 10
ml_constraints = 10

cluster_means = np.random.randint(data_range, size=nr_of_clusters)
cluster_stds = np.random.randint(low=1, high=data_range/10, size=nr_of_clusters)

data_generators = np.random.choice(nr_of_clusters, nr_of_datapoints)

data = []
data_by_gaussian = [[] for x in range(nr_of_clusters)]

for index, generator in enumerate(data_generators):
    point = np.random.normal(cluster_means[generator], cluster_stds[generator])
    data.append((index, point))
    data_by_gaussian[generator].append((index, point))

must_links = []
cannot_links = []

for i in range(cl_constraints):
    groups = np.random.choice(nr_of_clusters, 2, replace=False)
    point1 = random.choice(data_by_gaussian[groups[0]])
    point2 = random.choice(data_by_gaussian[groups[1]])
    cannot_links.append((point1, point2))

for i in range(ml_constraints):
    group = np.random.choice(nr_of_clusters)
    point1 = random.choice(data_by_gaussian[group])
    point2 = random.choice(data_by_gaussian[group])
    must_links.append((point1, point2))

f = open('out.txt','w')
for (i, point) in data:
    f.write('e ' + str(point) + '\n')
for ((i1, p1), (i2, p2)) in cannot_links:
    f.write('c ' + str(i1) + ' ' + str(i2) + '\n')
for ((i1, p1), (i2, p2)) in must_links:
    f.write('m ' + str(i1) + ' ' + str(i2) + '\n')
for i in range(nr_of_clusters):
    f.write('g ' + str(np.random.randint(data_range)) + ' ' + str(np.random.randint(low=1, high=data_range/2)) + ' ' + str(1.0/nr_of_clusters) + '\n')

f.close()