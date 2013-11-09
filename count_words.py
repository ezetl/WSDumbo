#!/usr/bin/env python
# -*- coding: utf-8 -*-
def mapper(key, value):
    l = [".", ")", "(", ",", ";", "...", '"',":", "-", "/", "\\", "'",
         "?", "!", "¡", "¿", "<", ">", "»", "«", "*", "|","²","°",
         "¨", "$"]
    for word in value.split():
        if word not in l:
            yield word.replace(".", ""), 1
        else:
            pass

def reducer(key, values):
#    s = sum(values)
#    if s>=100:
    yield key, sum(values)
#    else:
#    	pass

if __name__ == "__main__":
    import dumbo
    dumbo.run(mapper, reducer, combiner=reducer)
