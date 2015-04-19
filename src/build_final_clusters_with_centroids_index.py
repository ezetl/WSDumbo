import numpy as np

CLUSTERS_CENTROIDS = 'clusters_centroids.dat'
CONTEXTS = 'contexts.dat'

def load_clusters(filename):
    clusters = []
    f = open(filename, "r")
    lines = f.read().splitlines()
    for line in lines:
        aux = [np.float32(elem) for elem in line.split()]
        aux1 = np.array(aux, dtype=np.float32)
        clusters.append(aux1)
    return clusters

def load_contexts(filename):
    ctxt = []
    words = []
    f = open(filename, "r")
    lines = f.read().splitlines()
    for line in lines:
        aux = [np.float32(elem) for elem in line.split()[1:]]
        aux1 = np.array(aux, dtype=np.float32)
        ctxt.append(aux1)
        words.append(line.split()[0])
    return words, ctxt

def nearest_cluster_id(clusters, point):
    """
	Find the nearest neighbor
	Inputs:
	clusters: A numpy array of shape, (M,N) (N=Dims, M=NumClusters)
	point: A numpy array of shape (1,N) or (N,) (N=Dims,)
	Outputs:
	An int representing the nearest neighbor index into clusters.
	"""
    dist = point - clusters
    dist = np.sum(dist*dist,1)
    return int(np.argmin(dist))

def main():
	print "Loading files"
	centroids = load_clusters(CLUSTERS_CENTROIDS)
	words, contexts = load_contexts(CONTEXTS)
	print "Finish loading files"
	res = []
	print "Beggining process"
	for i, c in enumerate(contexts):
		w = words[i]
		index = nearest_cluster_id(centroids, c)
		#print index, w
		res.append((index, c))

	print "Process Finished"
	print "Writing results in a file"
	f = open("../results/resultados_clusters_con_indices.dat", "w")
	for k,v in res:
		s = ""
		for elem in v:
			s += str(elem) + "\t"
		f.write(str(k) + "\t" + s + "\n")
	f.close()
	print "END"

if __name__=="__main__":
	main()
