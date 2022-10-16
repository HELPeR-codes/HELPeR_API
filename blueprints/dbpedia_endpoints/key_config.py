
import spacy_dbpedia_spotlight
import sentence_transformers
# import spacy
from sentence_transformers import SentenceTransformer
import html2text
class config:
    nlpdb = spacy_dbpedia_spotlight.create('en')


    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.body_width = 10000

    # initialize sentence transformer model
    MODEL_EMBED = None
    MODEL_EMBED = SentenceTransformer('allenai-specter')

    debug=False

    #atleast 0.6 score
    sim_score=0.7

    #atleast 0.8 confidence
    link_score=0.8

    # Not these entity types
    types_not_allowed = set(['MilitaryUnit','Place', 'Species', 'Event','Website',  'Animal', 'Species', 'MusicalWork', 'Film','Location','Country'])

    #not_used_entities_file='/home/khushboo/role_classification/not_used_entities_file'
    #f_notusedwriter = open(not_used_entities_file,'w+')

