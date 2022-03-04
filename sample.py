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

# !pip install sentence_transformers -q
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
model_name = "facebook/bart-large-cnn" #phiyodr/bart-large-finetuned-squad2
# RameshArvind/roberta_long_answer_nq

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device = 0)

def get_answer(q):
    c = get_ctx(q)
    # print(c)
    QA_input = q + "[SEP]" + c
    QA_input = QA_input.split()
    QA_input = QA_input[0:700]
    QA_input = " ".join(QA_input)
    res = summarizer(QA_input, max_length=200, min_length=30)
    ans = ""
    for i in res:
        ans = ans + (i['summary_text'])
    return ans
