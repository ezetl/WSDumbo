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
#define CORPUS_PATH "../corpus/wiki_utf8"

using namespace std;
using namespace freeling;
namespace fs = boost::filesystem; 

int main (int argc, char **argv) {
    /**************************************************************************
     ***************************FREELING GENERAL SETUP*************************
     *************************************************************************/
    util::init_locale(L"es_AR.utf8");
    wstring ipath;
    ipath=L"/usr/local/";
    wstring lang=L"/es/";
    wstring path=ipath+L"/share/freeling"+lang;
    /* Create maco_options and analyzers */
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
    /* settings files for each module */
    opt.UserMapFile=L"";
    opt.LocutionsFile=path+L"locucions.dat";
    opt.AffixFile=path+L"afixos.dat";
    opt.ProbabilityFile=path+L"probabilitats.dat";
    opt.DictionaryFile=path+L"dicc.src";
    opt.NPdataFile=path+L"np.dat";
    opt.PunctuationFile=path+L"../common/punct.dat"; 
    opt.QuantitiesFile=path+L"quantities.dat";
    maco morfo(opt); 
    /* Create a tagger. It is important to set FORCE_TAGGER: it forces
     * Freeling to put a tag for each word */
    hmm_tagger tagger(path+L"tagger.dat", true, FORCE_TAGGER);
    /**************************************************************************
     *********************************END SETUP********************************
     *************************************************************************/

    fs::path targetDir(CORPUS_PATH); 
    fs::directory_iterator it(targetDir), eod;

    /*My corpus was splitted in several files, this may have to be
     * modified/simplified to fit your needs*/
    BOOST_FOREACH(fs::path const &p, std::make_pair(it, eod)){
        string corpus_name = p.string();
        wifstream corpus(corpus_name.c_str());
        if(!corpus){
            return -1;
        }
        string dest_cor = corpus_name.substr(17, corpus_name.size());
        dest_cor = DEST_PATH + dest_cor + ".utf8.lemma.txt";
        wofstream lemma_c(dest_cor.c_str());
        wstring text;
        wstring lemma;
        list<word> lw;
        list<sentence> ls;
        list<sentence>::iterator it;
        sentence::const_iterator wo;
        /* Get text using stdin while not EOF */
        while (getline(corpus, text)) {
            lw=tk.tokenize(text);
            /* Return sentences */
            ls=sp.split(lw, false);
            /* Morphosyntactic analysis and sense disambiguation */
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
            /* Ensure splitter does not retain any line  */
            ls.clear();
            lw.clear();
            sp.split(lw, true, ls);
        }
        lemma_c.close();
        corpus.close();
    }
    return 0;
}
