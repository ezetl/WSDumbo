#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import numpy as np
SEPARATOR = '\t'
COOCURR_SVD_V = 'coocurrences_svd.V'
WORDFILE = 'count_20000_wiki.dat'

class Mapper:
    def __init__(self):
        # We only want to build windows with relevant words
        # The words file ONLY contains words, not counts nor
        # another info
        f = open(WORDFILE, "r")
        self.words = set(line.strip() for line in f)
        f.close()

        f = open(WORDFILE, "r")
        self.dims = list(set([f.next().strip() for x in xrange(2000)]))
        f.close()

        f = open(COOCURR_SVD_V, "r")
        lines = f.read().splitlines()
        self.ctxs = []
        for line in lines:
            aux = [np.float32(elem) for elem in line.split()]
            aux1 = np.array(aux, dtype=np.float32)
            self.ctxs.append(aux1)
        # Neighbours to check, we're using 50 words window
        self.neighbs = 25

    def __call__(self, key, value):
        # Hadoop passes file lines as 'value', and each line
        # is a sentence, so this is ok.
        line = str(value).strip()
        line = line.translate(string.maketrans("",""), string.punctuation)
        words = line.split()
        context = np.zeros(shape=(100,), dtype=np.float32)
        can_process = len(words)>0
        if can_process:
            for i, w in enumerate(words):
                if w in self.words:
                    right = words[i+1 : min(i+self.neighbs, len(words)-1)+1]
                    left = words[max(0, i-self.neighbs) : i]
                    for wo in right:
                        if wo in self.dims:
                            context += self.ctxs[self.dims.index(wo)]
                    for wo in left:
                        if wo in self.dims:
                            context += self.ctxs[self.dims.index(wo)]
                    final_context = ""
                    for elem in context:
                        final_context += str(elem) + SEPARATOR
                    yield w, final_context
        else:
            pass

def runner(job):
    job.additer(Mapper)

def starter(prog):
	pass

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner,starter)