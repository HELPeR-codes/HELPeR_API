import blueprints
from nltk.stem import WordNetLemmatizer
import operator
import threading
from nltk.stem import PorterStemmer
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from blueprints.scispacy_endpoint.med_config import aconfig as config
semantic_types_allowed = config.semantic_types_allowed
from blueprints.scispacy_endpoint.med_utilities import scoring
nlpdb = config.NLP_sci
model = config.BioModelEmbed

print("load model")

class Stemmer(threading.local):

    def __init__(self):
        # wn.ensure_loaded()
        self.stem = PorterStemmer().stem

stemmer = Stemmer()

def stem(text):
    word_list = text.split(" ")
    for i in range(len(word_list)):
        word_list[i] = stemmer.stem(word_list[i])

    return ' '.join(word_list)


def preprocessText(text,stemming=False, lower=False):

    text = text.replace("\n"," ")
    text = re.sub("[ ]{1,}",r' ',text)

    text = re.sub(r'\W+|\d+', ' ', text.strip())
    tokens = word_tokenize(text)
    tokens = [token.strip().lower() for token in tokens ]
    if lower:
        text = text.lower()
    if stemming:
        tokens = [stem(token.strip()) for token in tokens]

    return " ".join(tokens)

def preprocessTextMin(text,stemming=False, lower=True):

    text = text.replace("\n"," ")
    text = re.sub("[ ]{1,}",r' ',text)

    # text = re.sub(r'\W+|\d+', ' ', text.strip())
    tokens = word_tokenize(text)
    tokens = [token.strip().lower() for token in tokens ]
    if lower:
        text = text.lower()
    if stemming:
        tokens = [stem(token.strip()) for token in tokens]

    return " ".join(tokens)




def keyphrase_sim(text, keyphrase_list=[],keyphrase_def={}):
    concept_weight = {}
    text = text.lower()
    text = preprocessText(text)

    for token in keyphrase_list:
        print(keyphrase_def[token])
        keyphrase_token = token + " " + keyphrase_def[token][4]
        sim2 = scoring( (keyphrase_token,text), config.BioModelEmbed )
        concept_weight[token] = sim2
    return concept_weight



lemmatizer = WordNetLemmatizer()

keyphrase_not_in=[]

# ['T091', 'T122', 'T019', 'T200', 'T060', 'T203', 'T047', 'T045', 'T028',
#                       'T093', 'T059', 'T034', 'T063', 'T114', 'T042', 'T046', 'T121', 'T184', 'T005', 'T127','T061',
#                      'T023']

keyphrase_not_in = ['cell','diagnosed','finding','diagnosis']
proc_keyphrase =  [ preprocessText(name,lower=True,stemming=True) for name in keyphrase_not_in]

def extract_med_key(n, text=None):
    concept_list = []
    concept_def = {}
    concept_list_process = []
    # print("sentence divided")
    doc = nlpdb(text)
    linker = nlpdb.get_pipe("scispacy_linker")
    for entity in doc.ents:
        if entity._.kb_ents is not None and len(entity._.kb_ents) > 0:

            umls_ent = entity._.kb_ents[0]

            score = umls_ent[1]
            name = str(entity).strip()
            process_name = preprocessText(name, lower=True, stemming=True)
            cui = linker.kb.cui_to_entity[umls_ent[0]]
            if cui[3][0] not in semantic_types_allowed:
                continue
            # print(cui[3][0], name)
            # and cui[3][0] in semantic_types_allowed
            if process_name in proc_keyphrase:
                continue

            print(cui[3][0], name, score,cui)
            if len(name) > 1 and score > 0.8:
                if process_name not in concept_list_process:
                    concept_list.append(name)

                    concept_list_process.append(process_name)
                    concept_def[name] = (entity.start_char, entity.end_char,cui[3][0],cui[0],cui[4])
    # print("concept extracted")
    concept_dict = keyphrase_sim(text, concept_list,concept_def)
    # print("concept similarity calculated")
    trunc_concept = list(sorted(concept_dict.items(), key=operator.itemgetter(1), reverse=True)[:n + 1])
    # print("sort and sent the coccepts")
    print(trunc_concept)
    return trunc_concept

if __name__ == '__main__':
    print("hi")
    text = "The patient has chest pain and was diagonised with high cholesterol. This can be an indicator of high blood pressure."
    extract_med_key(10, text)