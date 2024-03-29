# -*- coding: utf-8 -*-
'''
Created on 2012-11-23

@author: tianwei
Source:
https://github.com/tianweidut/CookBook/blob/master/hadoop/kmeans/kmeans.py
'''
import dumbo
import numpy as np

SEP = ' '  # Parse from file
CONTEXTS_FILE = '../results/init_clusters_noletters.dat'


class Mapper():

    def __init__(self):
        self.clusters = self._load_clusters()
        self.result = {}

    def _load_clusters(self):
        """
        Returns context list.
        """
        clusters = []
        f = open(CONTEXTS_FILE, "r")
        lines = f.read().splitlines()
        for line in lines:
            aux = [np.float32(elem) for elem in line.split()]
            aux1 = np.array(aux, dtype=np.float32)
            clusters.append(aux1)
        return clusters

    def _nearest_cluster_id(self, clusters, point):
        """
        Find the nearest neighbor
        Inputs:
        clusters: A numpy array of shape, (M,N) (N=Dims, M=NumClusters)
        point: A numpy array of shape (1,N) or (N,) (N=Dims,)
        Outputs:
        An int representing the nearest neighbor index into clusters.
        """
        dist = point - clusters
        dist = np.sum(dist * dist, 1)
        return int(np.argmin(dist))

    def _extend_point(self, point):
        """
        Add a new item, which show the number 1
        """
        point = np.resize(point, len(point) + 1)
        point[-1] = 1
        return point

    def __call__(self, data):
        """
        Mapper Program: which use in-mapper combiner

        Inputs:
        key: data , which is the whole artical

        Outputs:
        key: kinds
        value: the centroid
        """
        # local mapper
        for docID, doc in data:
            for term in doc.split("\n"):
                point = np.fromstring(term, dtype=np.float64, sep=SEP)
                n = self._nearest_cluster_id(self.clusters, point)
                point = self._extend_point(point)

                # in-mappper combiner
                self.result[n] = self.result.get(n, 0) + point

        # close yield
        for n, point in self.result.items():
            yield n, point

    def __call__singlemap(self, key, value):
        """
        Real Mapper Program : Take in a point , Find its NN
        Inputs:
        key: noused (Filename)
        value: point ,it is a string, we should make it a numpy array
        Outputs:
        A tuple in the form of (key,value)
        key: nearest cluster index (int)
        value: patial sum, it 1 now. (numpy array)
        """
        point = np.fromstring(value, dtype=np.float64, sep=SEP)
        n = self._nearest_cluster_id(self.clusters, point)
        point = self._extend_point(point)

        yield n, point.tolist()


class Reducer():

    def _computer_centroid(self, s):
        s = [i / s[-1] for i in s]
        return s

    def __call__(self, key, values):
        """
        Take in a serials of points , find their sum
        Input:
        key: nearest cluster index(int)
        points: patial sums (numpy array)
        Yields:
        A tuple in the form of (key,value)
        key: cluster index(int)
        value: cluster center (numpy array)
        """
        s = None
        for v in values:
            if s is None:
                s = [0] * len(v)
            s = [s[i] + v[i] for i in range(0, len(v))]
        m = self._computer_centroid(s)

        yield m[0:-1], "\t"

if __name__ == "__main__":
    dumbo.run(Mapper, Reducer)
