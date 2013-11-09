#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string

SEPARATOR = '\t'

class Mapper:
    def __init__(self):
        # We only want to build windows with relevant words
        f = open(self.params["words"], "r")
        self.words = set(line.split()[0] for line in f)
        f.close()
        # Neighbours to check, we're using 50 words window
        self.neighbs = 25

    def __call__(self, key, value):
        # Hadoop passes file lines as 'value', and each line
        # is a sentence, so this is ok.
        line = read_input(value)
        line = line.translate(string.maketrans("",""), string.punctuation)
        words = line.split()

        if(len(words)‪‪‪‪‪>0):
            for i, w in enumerate(words):
                if w in self.words:
                    dic = {}
                    right = words[i+1 : min(i+self.neighbs, len(a)-1)+1]
                    left = words[max(0, i-self.neighbs) : i]
                    for word in right:
                        if word in self.words:
                            if dic.get(word, 0)==0:
                                dic[word] = 1
                            else:
                                dic[word] += 1
                    for word in left:
                        if word in self.words:
                            if dic.get(word, 0)==0:
                                dic[word] = 1
                            else:
                                dic[word] += 1
                    yield word, dic
                else:
                    pass

    def read_input(value):
        # split the line into words
        yield value.strip()


class Reducer:
    def __init__(self):
        # We need this to build the final string containing all
        # coocurrences (even those that are zero).
        f = open(self.params["words"], "r")
        self.words = set(line.split()[0] for line in f)
        f.close()
        self.final_dic = {}

    def __call__(self, key, values):
        for dic in values:
            for k, v in dic:
                if final_dic.get(k, 0)==0:
                    final_dic[k] = v
                else:
                    final_dic[k] += v
        coocur = ""
        for elem in self.words:
            coocur += str(final_dic.get(elem, 0)) + SEPARATOR
        # Yield the first order coocurrence vector of key
        yield key, coocur

def runner(job):
    job.additer(Mapper,Reducer,Reducer)

def starter(prog):
    excludes = prog.delopt("words")
    if excludes:
        prog.addopt("param","words="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner,starter)
