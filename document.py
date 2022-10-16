import csv
from nltk.tokenize import sent_tokenize
import pandas as pd
import sys

class Document:
    def __init__(self,id,text,sentence_delimiter=None,type='txt',other_fields={}, *args, **kwargs):
        self.sentences = []
        self.npchunks = []
        self.type = "general"
        self.id = id
        self.text = text
        self.sentence_delimiter = sentence_delimiter
        self.type= type
        self.tokens = text.split(" ")
        self.otherfields=other_fields
        sen_list=[]
        if self.sentence_delimiter == None:
            sen_list = sent_tokenize(self.text)
        else:
            sen_list = self.text.split(self.sentence_delimiter)

        for sen in sen_list:
            self.sentences.append(sen)
            # print(sen)
        self.no_sent = len(self.sentences)

    def __str__(self):
        return '%s\t%s' % (self.id, self.text)

    def update(self,itext):
        self.text = self.text + ". " + itext
        sen_list= []
        if self.sentence_delimiter == None:
            sen_list = sent_tokenize(self.text)
        else:
            sen_list = self.text.split(self.sentence_delimiter)

        for sen in sen_list:
            self.sentences.append(sen)

        self.no_sent = len(self.sentences)




def load_document(path,booknames=[],textfield=['text'],idfield="id",otherfields=[],idelimiter=',',booknamefield='bookname'):
    print('Start loading documents from %s' % path)
    doc_list = []
    doc_list_dict= {}
    df = pd.read_csv(path,header=0,delimiter=idelimiter)

    for index,row in df.iterrows():
        if(len(booknames) == 0  or ( row[booknamefield].startswith(tuple(booknames)))):
            text = [ str(row[field]) for field in textfield]
            text = text  + [" "]
            otherfields_dict = { column:row[column] for column in df.columns if (column not in textfield and column != idfield and column in otherfields)}
            docid = str(row[idfield])

            doc_text = ' '.join(text)
            if docid in doc_list_dict:
                prevdoc = doc_list_dict[docid]
                prevdoc.update(doc_text)
                doc_list_dict[row[idfield]] = prevdoc
            else:
                doc = Document(docid, doc_text, otherfields=otherfields_dict)
                doc_list_dict[row[idfield]] = doc

    for docid in doc_list_dict:
        doc_list.append(doc_list_dict[docid])

    import csv

    with open('document.csv', 'w') as f:
        f.write("%s,%s\n" % ("docid", "text"))
        for docid in doc_list_dict:
            f.write("%s,%s\n" % (docid, doc_list_dict[docid]))

    return doc_list


def load_documentperline(path,sentence_delimiter=None):

    print('Start loading documents from %s' % path)
    doc_list = []

    with open(path) as fp:
        for cnt, line in enumerate(fp):
            # print("Line {}: {}".format(cnt, line))

            docid = str(cnt+1)
            doc_text = line
            doc = Document(docid, doc_text,sentence_delimiter)
            doc_list.append(doc)

    return doc_list

def load_document_filename(path,sentence_delimiter=None):

    print('Start loading documents from %s' % path)
    print(path)
    with open(path) as fp:
        docid = path
        doc_text = fp.read()
        doc = Document(docid, doc_text,sentence_delimiter)

    return doc