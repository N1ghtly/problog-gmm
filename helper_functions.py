import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def get_probabilities_per_evidence(gaussian, evidence):
    return map(lambda e: e.gaussian_probabilities[gaussian.id] ,evidence)

def get_probabilities_per_gaussian(evid, gaussians):
    return map(lambda g: evid.gaussian_probabilities[g.id], gaussians)

def get_remaining_evidence_with_dependency(evid, must_link, cannot_link, assignments):
    return filter(lambda e: e not in [e for (e, g) in assignments] , get_evidence_with_dependency(evid, must_link, cannot_link))

def get_evidence_with_dependency(evid, must_link, cannot_link):
    return list(get_linked_evidence_set(evid, must_link).union(get_linked_evidence_set(evid, cannot_link)))

def get_mixing_weight_given_possible_gaussians(gaussian, possible_gaussians):
    return gaussian.weight
    #return gaussian.weight / sum([g.weight for g in possible_gaussians])
    
def plot(evidence, gaussians):
    (fig, plt) = get_fig_plot(evidence, gaussians)
    plt.show()

def save_plot(name, evidence, gaussians):
    (fig, plt) = get_fig_plot(evidence, gaussians)
    plt.close(fig)
    fig.savefig('/home/xander/thesis/' + name + '.png')

def get_fig_plot(evidence, gaussians):
    plt.ioff()
    e_values = [e.value for e in evidence]
    buffer_size = (max(e_values) - min(e_values)) * 0.2
    x = np.linspace(min(e_values) - buffer_size, max(e_values) + buffer_size, 500)
    fig = plt.figure()
    for gaussian in gaussians:
        plt.plot(x,mlab.normpdf(x, gaussian.mean, gaussian.std))
    plt.plot(x, [sum([mlab.normpdf(v, gaussian.mean, gaussian.std) for gaussian in gaussians]) for v in x], '--')
    plt.plot(e_values, np.repeat([0], len(evidence)), 'ro')
    
    return (fig, plt)

def get_linked_evidence_set(evid, links):
    filtered_evidence = set()
    for constraint in links:
        if constraint.contains(evid):
            filtered_evidence.add(constraint.get_other(evid))
    return filtered_evidence

def get_linked_evidence(evid, links):
    return list(get_linked_evidence_set(evid, links))
            
def print_clusters(evidence, gaussians):
    print "Cluster    Evidence   Probability"
    evid_gaussian_probabilities = []
    for evid in evidence:
        evid_gaussian_probabilities.append([])
        for gaussian in gaussians:
            evid_gaussian_probabilities[-1].append(gaussian.get_density_value(evid))
    evid_gaussian_probabilities = map(lambda probs: [x/sum(probs) for x in probs], evid_gaussian_probabilities)

    for i, g in enumerate(gaussians):
        for h, evid_probs in enumerate(evid_gaussian_probabilities):
            if evid_probs[i] == max(evid_probs):
                print "{0:10} {1:10} {2:.1f} %".format(g, evidence[h], evid_probs[i]*100 )

def print_progress(gaussians):
    print "-----------------------------------------------------------------------------\nNew mixing weights (m values):"
    print [g.weight for g in gaussians]

    print "\nNew means:"
    print [g.mean for g in gaussians]

    print "\nNew stds:"
    print [g.std for g in gaussians]