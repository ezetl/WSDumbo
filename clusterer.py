import sys
import numpy as np
import nltk as nl
from nltk import cluster

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
    f = open("resultados_cluster.dat", "w")
    # Show data
    for i, elem in enumerate(clusters):
        a = "{} : {}".format(contexts[i][0], elem)
        f.write(a)
        print(a)
    f.close()
if __name__=="__main__":
    main()