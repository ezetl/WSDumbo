def mapper(key, value):
    for word in value.split():
        yield word, 1

def reducer(key, values):
    s = sum(values)
    if s>=100:
        yield key, s
    else:
        pass

if __name__ == "__main__":
    import dumbo
    dumbo.run(mapper, reducer, combiner=reducer)
