# -*- coding: UTF-8 -*-
import dumbo
import numpy as np
import os

SEP = '	' #Parse from file
CONTEXTS_FILE = 'little_clusters.dat'
class Mapper():
    def __init__(self):
        self.words, self.clusters = self._load_clusters()
        self.result = {}

    def _load_clusters(self):
        """
        Devuelve lista (palabra,context)
        """
        clusters = []
        words= []
        f = open(CONTEXTS_FILE, "r")
        lines = f.read().splitlines()
        for line in lines:
            aux = [np.float32(elem) for elem in line.split()[1:]]
            aux1 = np.array(aux, dtype=np.float32)
            clusters.append(aux1)
            words.append(line.split()[0])
        return words, clusters

    def _nearest_cluster_id(self,clusters, point):
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

    def _extend_point(self,point):
        """
        Add a new item, which show the number 1
        """
        point = np.resize(point, len(point)+1)
        point[-1] = 1
        return point

    def __call__(self,key, value):
        """
        Mapper Program: which use in-mapper combiner

        Inputs:
        key: data , which is the whole artical

        Outputs:
        key: kinds
        value: the centroid
        """
        #local mapper
#        for docID,doc in data:
#            for term in doc.split("\n"):
        t = value.split()
        word = t[0]
        point = np.array(t[1:],dtype=np.float32)
#                n = self._nearest_cluster_id(self.clusters,point)
        n = 4
        point = self._extend_point(point)

        #in-mappper combiner
        if self.result.get(n, None) is not None:
            self.result[n][0] = self.result[n][0] + point
            self.result[n][1].append(word)
        else:
            self.result[n] = [point, [word]]

        #close yield
        for n, point_words in self.result.items():
            yield (n, point_words)

#    def __call__singlemap(self,key,value):
#        """
#        Real Mapper Program : Take in a point , Find its NN
#        Inputs:
#        key: noused (Filename)
#        value: point ,it is a string, we should make it a numpy array
#        Outputs:
#        A tuple in the form of (key,value)
#        key: nearest cluster index (int)
#        value: patial sum, it 1 now. (numpy array)
#        
#        """
#        point, words = value
#        point = np.fromstring(point,dtype=np.float32,sep=SEP)
##        n = self._nearest_cluster_id(self.clusters, point)
#        n = 4
##        point = self._extend_point(point)

#        yield n, (point.to_list(), list(set(words)))

class Reducer():
    def _computer_centroid(self,s):
        s = [i /s[-1] for i in s]

    def __call__(self,key,values):
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
        words = set()
        for v in values:
            point, wordlist = v
            for elem in wordlist:
                words.add(elem)
            if s is None:
                s = [0] * len(point)
            s = [s[i] + point[i] for i in range(0,len(point))]
        m = self._computer_centroid(s)
        
        stringwords=""
        for w in words:
            stringwords += w + " "
        yield m[0:-1], stringwords 


if __name__ == "__main__":
    dumbo.run(Mapper) 
