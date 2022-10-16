from sentence_transformers import SentenceTransformer

import spacy
from scispacy.linking import EntityLinker
from scispacy.umls_linking import UmlsEntityLinker



class aconfig:
    EN = None
    NLP_sci = spacy.load("en_core_sci_scibert")
    NLP_sci.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    # BioModelEmbed = FastText('/home/khushboo/role_classification/BioWordVec_PubMed_MIMICIII_d200.bin')
    #'T109', 'T185'
    semantic_types_allowed = ['T005', 'T019', 'T028', 'T034', 'T044','T045','T046','T047', 'T059', 'T060', 'T061', 'T063','T116','T185','T121', 'T122', 'T127', 'T184',
                           'T200', 'T203', 'T191', 'T190','T201' ]

    BioModelEmbed = None
    BioModelEmbed = SentenceTransformer('gsarti/biobert-nli')
