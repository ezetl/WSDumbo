#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <cstring>
#include <iomanip>
#include <boost/filesystem.hpp>
#include <boost/foreach.hpp>

#include "freeling.h"
#include "freeling/morfo/traces.h"
#define DEST_PATH "../corpus/corpus_lemmas/"

using namespace std;
using namespace freeling;
namespace fs = boost::filesystem; 

int main (int argc, char **argv) {
    /***************************************************************************
        **************************SETUP GENERAL DE FREELING*************************
        ***************************************************************************/
    /*Setear con su lenguaje de confianza */
    util::init_locale(L"es_AR.utf8");
    wstring ipath;
    ipath=L"/usr/local/";
    wstring lang=L"/es/";
    wstring path=ipath+L"/share/freeling"+lang;
    /* Creamos analizadores y un maco_options*/
    tokenizer tk(path+L"tokenizer.dat");
    splitter sp(path+L"splitter.dat");
    maco_options opt(L"es");
    opt.UserMap=false;
    opt.QuantitiesDetection = true;
    opt.AffixAnalysis = true;
    opt.MultiwordsDetection = true;
    opt.NumbersDetection = true;
    opt.PunctuationDetection = true;
    opt.DatesDetection = true;
    opt.DictionarySearch = true;
    opt.ProbabilityAssignment = true;
    opt.NERecognition = true;
    /* Y ahora los archivos de configuracion de cada modulo*/
    opt.UserMapFile=L"";
    opt.LocutionsFile=path+L"locucions.dat";
    opt.AffixFile=path+L"afixos.dat";
    opt.ProbabilityFile=path+L"probabilitats.dat";
    opt.DictionaryFile=path+L"dicc.src";
    opt.NPdataFile=path+L"np.dat";
    opt.PunctuationFile=path+L"../common/punct.dat"; 
    opt.QuantitiesFile=path+L"quantities.dat";
    /*Creamos el analizador con el maco options*/
    maco morfo(opt); 
    /*Creamos un tagger. Es importante la opcion FORCE_TAGGER, pues 
    * obliga a poner un tag por palabra*/
    hmm_tagger tagger(path+L"tagger.dat", true, FORCE_TAGGER);
    /***************************************************************************
        **********************************FIN SETUP*********************************
        ***************************************************************************/
    fs::path targetDir("../corpus/wiki_utf8"); 
    fs::directory_iterator it(targetDir), eod;

    BOOST_FOREACH(fs::path const &p, std::make_pair(it, eod)){
        string corpus_name = p.string();
        wifstream corpus(corpus_name.c_str());
        if(!corpus){
            return -1;
        }
        string dest_cor = corpus_name.substr(17, corpus_name.size());
        /*Hola soy negro*/
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor.erase(dest_cor.size()-1);
        dest_cor = DEST_PATH + dest_cor + ".utf8.lemma.txt";
        wofstream lemma_c(dest_cor.c_str());
        wstring text;
        wstring lemma;
        list<word> lw;
        list<sentence> ls;
        list<sentence>::iterator it;
        sentence::const_iterator wo;
        /*Obtener texto por stdin a mientras no haya EOF*/
        while (getline(corpus, text)) {
            /*Primero tokenizamos la linea*/
            lw=tk.tokenize(text);
            /*Devolvemos la lista de oraciones de la linea ingresada*/
            ls=sp.split(lw, false);
            /*Analisis morfosintactico y desambiguacion de palabras*/
            morfo.analyze(ls);

            for(it=ls.begin(); it!=ls.end(); it++){
                for(wo=it->begin(); wo!=it->end(); wo++){
                    lemma = wo->get_lemma();
                    if(lemma!=L"."){
                        lemma_c << L" ";
                    }
                    lemma_c << lemma;
                }
            }
            lemma_c << endl;
            /*asegurarse de que el splitter no guarde alguna linea */
            ls.clear();
            lw.clear();
            sp.split(lw, true, ls);
        }
        lemma_c.close();
        corpus.close();
        cout << "Finalizado proceso de "<< dest_cor <<endl;
    }
    return 0;
}
