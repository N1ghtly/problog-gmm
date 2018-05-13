import algorithm
from must_link import MustLinkConstraint 
from cannot_link import CannotLinkConstraint 
from evidence import Evidence
from gaussian import Gaussian
from dataset import *

gaussians = generate_initial_gaussians(20, 10, 100)

evidence = generate_evidence()

must_link = []
cannot_link = []

options = dict()
options['ITERATIONS'] = 5
options['SAVE_PROGRESS_PNGS'] = False
options['SHOW_FINAL_PLOT'] = True
options['MIN_STANDARD_DEVIATION'] = 0.5
options['PRINT_CLUSTERS'] = True
options['DEBUG_OUTPUT'] = False
options['PRINT_PROGRESS'] = True

algorithm.run(gaussians, evidence, must_link, cannot_link, options)