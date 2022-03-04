# -*- coding: utf-8 -*-
"""s1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nBNRJZ5vPuC8Z76EzuD9YVPRp3pJw26l
"""

import json
 
f = open('data.json')
data = json.load(f)
d = ""
for i in data:
    # print()
    d = d + '\n '.join(data[i])
data = d

import nltk
from nltk import tokenize
nltk.download('punkt')
def split_to_sent(p):
    return tokenize.sent_tokenize(p)
data_sents = split_to_sent(data)

!pip install sentence_transformers -q
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
s_model = SentenceTransformer('bert-base-nli-mean-tokens').to("cuda")

def get_ctx(question, data_sents = data_sents, top = 50):
    sentences = [question]
    sentences.extend(data_sents)
    sentence_embeddings = s_model.encode(sentences)
    # print(sentence_embeddings.shape)
    simi = cosine_similarity(
    [sentence_embeddings[0]],
    sentence_embeddings[1:]
    )
    values,indices = torch.Tensor(simi).topk(top)

    indices = (indices[0])
    ctx = ""
    for i in indices:
        ctx = ctx + ". " + data_sents[i]
    return ctx

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
model_name = "deepset/roberta-base-squad2" #phiyodr/bart-large-finetuned-squad2
# RameshArvind/roberta_long_answer_nq

nlp = pipeline('question-answering', model=model_name, tokenizer=model_name, device = 0)

def nest_sentences(document,chunk_length):
    nested = []
    sent = []
    length = 0
    for sentence in nltk.sent_tokenize(document):
        length += len(sentence.split(" "))
        if length < chunk_length:
            sent.append(sentence)
        else:
            nested.append(" ".join(sent))
            sent = []
            sent.append(sentence)
            length = 0
    if len(sent)>0:
        nested.append(" ".join(sent))
    return nested

def get_answer(q):
    c = get_ctx(q)
    # print(c)
    QA_input = {
        'question': q,
        'context': data,
    }
    res = nlp(QA_input, topk = 3, doc_stride = 128, max_answer_len = 50)
    ans = ""
    done = []
    for i in res:
        if i['answer'] in done:
            continue
        ans = ans + "\n " + i['answer'] 
        done.append(i['answer'])
    return ans

# q = "What is the best institute in India?"
# a = get_answerv1(q)

# print(a)

# def get_answerv2(q):
#     chunks = nest_sentences(data, 512)
#     answers = []
#     for i in chunks:
#         QA_input = {
#             'question': q,
#             'context': i
#         }
#         res = nlp(QA_input)
#         # print(res['answer'])
#         answers.append(res['answer'])
#     answers.append(get_answerv1(q))
#     print(get_answerv1(q))
#     answer = get_ctx(q, (answers), 2)
#     return answer

# import transformers
# nlp_conv = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
# def get_answer_conv(question):
#     return str(nlp_conv(transformers.Conversation(question))).split("\nbot >> ")[1]

# from transformers import BartTokenizer, BartForQuestionAnswering
# import torch

# tokenizer = BartTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
# model = BartForQuestionAnswering.from_pretrained('valhalla/bart-large-finetuned-squadv1')

# question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"
# encoding = tokenizer(question, text, return_tensors='pt')
# input_ids = encoding['input_ids']
# attention_mask = encoding['attention_mask']

# start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]

# all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
# answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
# answer = tokenizer.convert_tokens_to_ids(answer.split())
# answer = tokenizer.decode(answer)
# #answer => 'a nice puppet'

# answer

# from transformers import BartTokenizer, BartForQuestionAnswering
# import torch
# tokenizer = BartTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
# model = BartForQuestionAnswering.from_pretrained('valhalla/bart-large-finetuned-squadv1').to("cuda")

# def get_answer_ext(question):
#     text = get_ctx(question)
#     # print(len(text))
#     encoding = tokenizer(question, text, return_tensors='pt').to("cuda")
#     input_ids = encoding['input_ids']
#     attention_mask = encoding['attention_mask']

#     start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]

#     all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
#     answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
#     answer = tokenizer.convert_tokens_to_ids(answer.split())
#     answer = tokenizer.decode(answer)
#     return answer

# q = "What are the objective of AICET?"
# get_answer_ext(q)

# get_answerv1(q)


