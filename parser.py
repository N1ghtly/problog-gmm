from must_link import MustLinkConstraint 
from cannot_link import CannotLinkConstraint 
from evidence import Evidence
from gaussian import Gaussian

def parse(filename):
    lines = (line.rstrip('\n') for line in open(filename, 'r'))

    evidence = []
    gaussians = []
    mustlink = []
    cannotlink = []

    for line in lines:
        parts = line.split(' ')
        if parts[0] == 'g':
            gaussians.append(Gaussian(float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == 'e':
            evidence.append(Evidence(float(parts[1])))
        elif parts[0] == 'c':
            cannotlink.append(CannotLinkConstraint(evidence[int(parts[1])], evidence[int(parts[2])]))
        elif parts[0] == 'm':
            mustlink.append(MustLinkConstraint(evidence[int(parts[1])], evidence[int(parts[2])]))
    
    return (evidence, gaussians, mustlink, cannotlink)