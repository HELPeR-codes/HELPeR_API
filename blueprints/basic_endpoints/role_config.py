from transformers import DistilBertForSequenceClassification

role_model_folder = './models/roles/'


columns = ["advice",
           'referral',
           'fact or situation appraisal',
           'personal Experience',
           'opinion',
           'emotional',
           ]


def load_rolemodels():
    role_model = {}

    for column_name in columns:
        print("model Loaded",column_name)
        role_model[column_name] = DistilBertForSequenceClassification.from_pretrained(
            role_model_folder + column_name.replace(" ", "_") + '/' + 'final_model.pt')
        role_model[column_name].eval()
    return role_model

from transformers import DistilBertTokenizerFast

class rconfig:
    import spacy
    NLP_role = spacy.load("en_core_web_sm")
    role_models = load_rolemodels()

    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    columns = ["advice",
               'referral',
               'fact or situation appraisal',
               'personal Experience',
               'opinion',
               'emotional',
               ]

