
import spacy_dbpedia_spotlight
import sentence_transformers
# import spacy
from sentence_transformers import SentenceTransformer
class config:
    nlpdb = spacy_dbpedia_spotlight.create('en')
    # nlpdb.add_pipe('dbpedia_spotlight')
    # nlpdb = spacy.load('en_core_web_lg')
    # Use your endpoint: don't put any trailing slashes, and don't include the /annotate path
    # nlpdb.add_pipe('dbpedia_spotlight', config={'dbpedia_rest_endpoint': 'http://localhost:2222/rest'})
    # nlpdb.add_pipe('dbpedia_spotlight', config={'process': 'candidates'})

    # from embedding_as_service.text.encode import Encoder
    # EN = Encoder(embedding='bert', model='bert_base_cased', max_seq_length=256)

    MODEL_EMBED = None
    # initialize sentence transformer model
    MODEL_EMBED = SentenceTransformer('allenai-specter')

    debug=False
    IR_CORPUS = 'data/iirmirbook.tsv'
    KC_CORPUS = 'data/conceptdocs.csv'
    IS_STEM=True
    REMOVE_STOPWORDS=True
    STOPWORD_PATH = 'data/stopword/stopword_en.txt'
    TRIE_CACHE_DIR = 'data/triecache/'

    #
    dir_sep = "/"
    file_ext =".concept"
    # Models

    # Concepts
    TFIDF = 'tfidf'
    TFIDFNP = 'tfidfnp'
    NGRAMS = 'ngrams'
    LIST_FILTER = 'list_filter'
    WIKI_FILTER = 'wiki_filter_np'
    LDA='LDA'
    LIST_FILTER_TFIDFNP="list_filter_np"
    GENERAL_CORPUS_TFIDFNP='wiki_tifidfnp'

    # LIST
    wiki_list='data/wordlist/wikipedia_14778209.txt.1'
    irbook_glossary_list = 'data/wordlist/irbook_glossary_707.txt'
    wiki_link  = 'data/wordlist/link.txt'
    expert_ann_list = 'data/wordlist/expert_list'
    glossary='data/wordlist/glossary_list.txt'
    mengdi_ngram_glossary = 'data/wordlist/mengdi_ngram_glossary.txt'
    iir_ground_truth = 'data/wordlist/iir_ground_truth.txt'
    wiki_title='data/wiki/wiki_titles'
    temp_list = 'data/wordlist/wordlist2.txt'
    Remove_Prev_models = False