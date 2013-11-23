# -*- coding: UTF-8 -*-

def main():
    res = []
    partial = {}
    f = open("contexts.dat", "r")
    lines = f.read().splitlines()
    for line in lines:
        l = line.split()
        if partial.get(l[0], 0) != 0:
            if partial.get(l[0], 0) == 1:
                partial[l[0]] += 1
                res.append(line)
        else:
            partial[l[0]] = 1
            res.append(line)
    f.close()
    f = open("min_contexts.dat", "w")
    for r in res:
        f.write(str(r))
        f.write("\n")
    f.close()

if __name__=="__main__":
    main()
