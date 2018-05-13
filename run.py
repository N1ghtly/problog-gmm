import time
import algorithm
from parser import *
from dataset import *

(evidence, gaussians, must_link, cannot_link) = parse('out.txt')

options = dict()
options['ITERATIONS'] = 10
options['SAVE_PROGRESS_PNGS'] = False
options['SHOW_FINAL_PLOT'] = False
options['MIN_STANDARD_DEVIATION'] = 0.2
options['DEBUG_OUTPUT'] = False
options['PRINT_CLUSTERS'] = False
options['PRINT_PROGRESS'] = False

start_time = time.time()

algorithm.run(gaussians, evidence, must_link, cannot_link, options)

print("--- %s seconds ---" % (time.time() - start_time))