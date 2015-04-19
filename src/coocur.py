#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
SEPARATOR = '\t'
# File with 20000 words in the order they appeared in the corpus.
# I reduced the number of words only for simplicity.
WORDFILE = 'count_20000_wiki.dat'


class Mapper:
    def __init__(self):
        # We only want to build windows with relevant words
        # The words file ONLY contains words (not counts, etc)
        f = open(WORDFILE, "r")
        self.words = set(line.strip() for line in f)
        f.close()

        f = open(WORDFILE, "r")
        self.dims = set([f.next().strip() for x in range(2000)])
        f.close()
        # Neighbours to check, we're using 50 words window
        self.neighbs = 25

    def __call__(self, key, value):
        # Hadoop passes file lines as 'value', and each line
        # is a sentence, so this is ok.
        line = str(value).strip()
        line = line.translate(string.maketrans("", ""), string.punctuation)
        words = line.split()
        can_process = len(words) > 0
        if can_process:
            for i, w in enumerate(words):
                if w in self.words:
                    dic = {}
                    right = words[i+1: min(i+self.neighbs, len(words)-1)+1]
                    left = words[max(0, i-self.neighbs): i]
                    for wo in right:
                        if wo in self.dims:
                            if dic.get(wo, -1) == -1:
                                dic[wo] = 1
                            else:
                                dic[wo] += 1
                    for wo in left:
                        if wo in self.dims:
                            if dic.get(wo, -1) == -1:
                                dic[wo] = 1
                            else:
                                dic[wo] += 1
                    yield w, dic
        else:
            pass


class Reducer:
    def __init__(self):
        # We need this to build the final string containing all
        # coocurrences (even those that are zero).
        self.final_dic = {}
        f = open(WORDFILE, "r")
        self.dims = set([f.next().strip() for x in range(2000)])
        f.close()

    def __call__(self, key, values):
        for dic in values:
            for k, v in dic.iteritems():
                if self.final_dic.get(k, -1) == -1:
                    self.final_dic[k] = v
                else:
                    self.final_dic[k] += v
        coocur = ""
        for elem in self.dims:
            coocur += str(self.final_dic.get(elem, 0)) + SEPARATOR
        # Yield the first order coocurrence vector of key
        yield key, coocur


def runner(job):
    job.additer(Mapper, Reducer)


def starter(prog):
	pass

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
