
from torch.utils.data import DataLoader
import numpy as np
import torch
from scipy.special import softmax

from blueprints.basic_endpoints.role_config import rconfig

roles=rconfig.columns

class TextEncodedDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def create_ds(df, tokenizer,column_name):
    labels = df[column_name].values
#     print(labels)
    text = df["text"].tolist()
    encodings = tokenizer(text, truncation=True, padding=True)
    ds = TextEncodedDataset(encodings, labels)
    return ds


# infer using sentence level : this was done for opinion as opinions are found more reliably using sentence level inference
def sent_infer(input_text, model, model_advice,tokenizer,nlp_role):
    infer_list = {}
    infer_list[0] = []
    infer_list[1] = []
    no_sent = True
    classp = 0
    input_text = input_text.replace("\n", " ")
    for sent in list(nlp_role(str(input_text)).sents):
        if len(str(sent).strip().split(" ")) > 3:
            no_sent = False

            # advice
            inputs_advice = tokenizer(str(sent), truncation=True, padding=True, return_tensors="pt")
            labels_advice = torch.tensor([1]).unsqueeze(0)  # Batch size 1
            outputs_advice = model_advice(**inputs_advice, labels=labels_advice)
            loss_advice = outputs_advice.loss
            logits_advice = outputs_advice.logits
            probs_advice = softmax(logits_advice.detach().numpy())
            #         print(probs)
            classp_advice = np.argmax(probs_advice)

            if classp_advice == 1:
                infer_list[classp].append(0)
                classp = 0
                continue
            inputs = tokenizer(str(sent), truncation=True, padding=True, return_tensors="pt")
            labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
            outputs = model(**inputs, labels=labels)
            # loss = outputs.loss
            logits = outputs.logits
            probs = softmax(logits.detach().numpy())
            #         print(probs)
            classp = np.argmax(probs)
            infer_list[classp].append(probs[0][classp])
    #             print(str(sent),classp)
    classp = 0
    if len(infer_list[1]) > 0:
        if max(infer_list[1]) > 0.60:
            classp = 1
        else:
            classp = 0

    if no_sent == True:
        infer_list[0].append(1)
    #     print(infer_list)
    return classp


# Infer with the whole text together
def infer(input_text, model,tokenizer):
    inputs = tokenizer(input_text, truncation=True, padding=True, return_tensors="pt")

    labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
    outputs = model(**inputs, labels=labels)
    # loss = outputs.loss
    logits = outputs.logits
    classp = np.argmax(softmax(logits.detach().numpy()))
    return classp

def extract_roles(text,nlp_role,role_models,rtokenizer):

    role_output = { role:0 for role in roles}

    if text is None:
        return role_output

    for column_name in roles:
        if column_name == 'opinion':
            role_output[column_name] = sent_infer(text, role_models[column_name],role_models['advice'],rtokenizer,nlp_role)
        else:
            role_output[column_name] = infer(text, role_models[column_name],rtokenizer)

    no_class = True
    for column_name in roles:
        if role_output[column_name] == 1:
            no_class = False
            break
    if no_class == True:
        role_output['other'] = 1

    return role_output
