import itertools
from helper_functions import *

class Evidence:
    newid = itertools.count().next

    def __init__(self, value):
        self.value = value
        self.id = Evidence.newid()
        self.density_values = []
        self.gaussian_probabilities = []

    def calculate_density_values(self, gaussians):
        self.density_values = [g.get_density_value(self) for g in gaussians]

    def calculate_gaussian_probabilities(self, gaussians, must_link, cannot_link, depending_evidence, evid_to_gaussian_assignments):
        # print "----\nCalculating all probabilities for " + str(self) + " with assignments " + str(evid_to_gaussian_assignments)
        possible_gaussians = self.get_possible_gaussians(gaussians, must_link, cannot_link, evid_to_gaussian_assignments)
        # print "Possible gaussians: " + str(possible_gaussians)

        total_probability = 0
        for g in possible_gaussians:
            p = self.calculate_gaussian_probability(gaussians, g, must_link, cannot_link, possible_gaussians, depending_evidence, evid_to_gaussian_assignments)
            # print "Calculated for " + str(self) + " that probability for " + str(g) + " = " + str(p)
            total_probability += p
        return total_probability

    def calculate_gaussian_probability(self, gaussians, g, must_link, cannot_link, possible_gaussians, depending_evidence, evid_to_gaussian_assignments):
        p = self.density_values[g.id]*get_mixing_weight_given_possible_gaussians(g, possible_gaussians)
        
        new_evid_to_gaussian_assignments = evid_to_gaussian_assignments[:]
        new_evid_to_gaussian_assignments.append((self, g))

        print new_evid_to_gaussian_assignments

        dep = self.calculate_depending_gaussians_probability(gaussians, g, must_link, cannot_link, depending_evidence, new_evid_to_gaussian_assignments)
        return dep*p


    def calculate_depending_gaussians_probability(self, gaussians, gaussian, must_link, cannot_link, depending_evidence, evid_to_gaussian_assignments):
        p = 1
        
        depending_evidence.update(get_remaining_evidence_with_dependency(self, must_link, cannot_link, evid_to_gaussian_assignments))
        #print depending_evidence
        if len(depending_evidence) == 0:
            return 1;
        evid = depending_evidence.pop()
        probability = evid.calculate_gaussian_probabilities(gaussians, must_link, cannot_link, depending_evidence, evid_to_gaussian_assignments)
        p *= probability
        return p

    def get_possible_gaussians(self, gaussians, must_link, cannot_link, evid_to_gaussian_assignments):
        must_link_evidence = get_linked_evidence(self, must_link)
        cannot_link_evidence = get_linked_evidence(self, cannot_link)

        # Copy list
        possible_gaussians = gaussians[:]

        for (evid, gaussian) in evid_to_gaussian_assignments:
            # If we already assigned the evidence a specific gaussian, only that gaussian is possible.
            if self == evid:
                possible_gaussians = [gaussian]
            # If there is a must-link constraint, we filter out all other gaussians
            if evid in must_link_evidence:
                possible_gaussians = filter(lambda g: g == gaussian, possible_gaussians)
            # If there is a cannot-link constraint, we filter out that assigned gaussian
            if evid in cannot_link_evidence:
                possible_gaussians = filter(lambda g: g != gaussian, possible_gaussians)

        return possible_gaussians

    
    def calculate_unconstrained_gaussian_probabilities(self, gaussians):
        weighted_probabilities = map(lambda g: self.density_values[g.id]*g.weight, gaussians)
        self.gaussian_probabilities = [p / sum(weighted_probabilities) for p in weighted_probabilities]

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "E(" + str(self.value) + ")"

    def __repr__(self):
        return "E(" + str(self.value) + ")"

    def __hash__(self):
        return self.id