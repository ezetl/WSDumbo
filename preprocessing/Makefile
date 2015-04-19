# directories where freeling and boost are installed
FREELINGDIR=/usr/local
BOOSTINCLUDEDIR=/usr/local/include
BOOSTLIBDIR=/usr/local/lib

PATHS=-L$(FREELINGDIR)/lib -I$(FREELINGDIR)/include -L$(BOOSTLIBDIR) -I$(BOOSTINCLUDEDIR)

all: transform_corpus

transform_corpus: transform_corpus.cpp
	g++ -o transform_corpus transform_corpus.cpp -lfreeling -L/usr/lib/ -lboost_system -L/usr/lib/ -lboost_filesystem $(PATHS)

clean:
	rm -f transform_corpus main
