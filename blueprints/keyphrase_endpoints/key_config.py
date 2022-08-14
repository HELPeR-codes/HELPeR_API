

class config:
    import pip install spacy-dbpedia-spotligh
    nlpdb = spacy_dbpedia_spotlight.create('en')
    # nlpdb.add_pipe('dbpedia_spotlight')

    from embedding_as_service.text.encode import Encoder
    EN = Encoder(embedding='bert', model='bert_base_cased', max_seq_length=256)


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