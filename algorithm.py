import math
import numpy as np
from helper_functions import *

def get_depending_evidence(evid, must_link, cannot_link):
    evidence = set()
    evidence.add(evid)

    while(True):
        new_evidence = set(evidence)
        for evid in evidence:
            deps = get_evidence_with_dependency(evid, must_link, cannot_link)
            new_evidence.update(deps)
        if len(new_evidence) == len(evidence):
            return new_evidence
        else:
            evidence = new_evidence

def get_possible_assignments(evidence, gaussians):
    assignments = [[]]
    for e in evidence:
        new_assignments = []
        for a in assignments:
            for g in gaussians:
                new_a = a[:]
                new_a.append((e, g))
                new_assignments.append(new_a)
        assignments = new_assignments
    return assignments

def get_possible_assignments_with_fixed(evidence, gaussians, fixed):
    ev = set(evidence)
    (e, g) = fixed
    ev.remove(e)
    assignments = [[fixed]]
    for e in ev:
        new_assignments = []
        for a in assignments:
            for g in gaussians:
                new_a = a[:]
                new_a.append((e, g))
                new_assignments.append(new_a)
        assignments = new_assignments
    return assignments

def are_constraints_satisfied((e, g), assignments, must_link, cannot_link):
    must_link_evidence = get_linked_evidence(e, must_link)
    cannot_link_evidence = get_linked_evidence(e, cannot_link)

    for (evid, gaussian) in assignments:
        if e == evid:
            continue
        if evid in must_link_evidence and gaussian != g:
            return 0
        if evid in cannot_link_evidence and gaussian == g:
            return 0
    return 1

def calculate_probability_of_assignment(assignment, must_link, cannot_link):
    p = 1
    for (e, g) in assignment:
        p *= e.density_values[g.id]*g.weight * are_constraints_satisfied((e, g), assignment, must_link, cannot_link)
    return p

def run(gaussians, evidence, must_link, cannot_link, options):
    for iteration in range(options['ITERATIONS']):
        for evid in evidence:
            evid.calculate_density_values(gaussians)
        
        for evid in evidence:
            
            #print '\n\n'
            #print 'For evid: ' + str(evid)
            depending_evidence = get_depending_evidence(evid, must_link, cannot_link)
            
            all_possible_assignments = get_possible_assignments(depending_evidence, gaussians)
            total = sum([calculate_probability_of_assignment(a, must_link, cannot_link) for a in all_possible_assignments])

            p = []
            for g in gaussians:
                possible_assignments = get_possible_assignments_with_fixed(depending_evidence, gaussians, (evid, g))
                probability = sum([calculate_probability_of_assignment(a, must_link, cannot_link) for a in possible_assignments])
                p.append(probability / total)
            evid.gaussian_probabilities = p

        if options['DEBUG_OUTPUT']:
            print "\n\nGaussians"
            print gaussians
            print "--------------------\nEvidence"
            for e in evidence:
                print e.gaussian_probabilities

        for g in gaussians:
            # Recalculate weight
            g.weight = sum(get_probabilities_per_evidence(g, evidence))/len(evidence)

            # Recalculate mean and std
            probabilities = get_probabilities_per_evidence(g, evidence)
            evidence_values = [e.value for e in evidence]
            probabilities_times_value = np.multiply(probabilities, evidence_values)
            g.mean = sum(probabilities_times_value)/sum(probabilities)
            g.std = max(math.sqrt(sum(np.multiply(probabilities, [(e - g.mean)**2 for e in evidence_values]))/sum(probabilities)), options['MIN_STANDARD_DEVIATION'])
        
        if options['SAVE_PROGRESS_PNGS']:
            save_plot("Iteration" + str(iteration), evidence, gaussians)
        if options['PRINT_PROGRESS']:
            print_progress(gaussians)
        if options['PRINT_CLUSTERS'] and iteration == options['ITERATIONS'] - 1:
            print_clusters(evidence, gaussians)

    if options['SHOW_FINAL_PLOT']:
        plot(evidence, gaussians)
