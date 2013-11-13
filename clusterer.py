import sys
import numpy as np
import nltk as nl
from nltk import cluster
from itertools import groupby
from operator import itemgetter

def main():
    try:
        f = open("contexts_head.dat", "r")
        lines = f.read().splitlines()
        f.close()
    except IOError:
        print("Couldn't find contexts file.")
        sys.exit(-1)
    # Load data to memory, this can take a while
    contexts = []
    for line in lines:
        l = line.split()
        values = []
        word = l[0]
        for v in l[1:]:
            values.append(np.float32(v))
        contexts.append((word, np.array(values)))
    only_values = []
    for elem in contexts:
        only_values.append(elem[1])

    # Begin clustering
    clusterer = cluster.GAAClusterer(4)
    clusters = clusterer.cluster(only_values, True)
    final_clusters = []
    for i, elem in enumerate(clusters):
        final_clusters.append((contexts[i][0], elem))
    f = open("resultados_cluster.dat", "w")
    for clus, group in groupby(final_clusters, itemgetter(1)):
        print str(clus) + ":"
        for word, clust in group:
            print word
    f.close()
if __name__=="__main__":
    main()