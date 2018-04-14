# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 20:41:49 2018

@author: shubham
"""

import nltk
from status import QnAStatus
import pickle

print("start")
nltk.download("punkt")
nltk.download("stopwords")
print("finish")

useless_words = nltk.corpus.stopwords.words("english")
start_words = ["who", "what", "when", "where", "why", "how", "is", "can", "does", "do" , "i" , "?"]

def build_bag_of_words_features_filtered(question):
    question = question.lower()
    token_words = nltk.word_tokenize(question)
    #print(token_words)
    token_words = [word for word in token_words if not word in useless_words]
    #print(token_words)
    token_words = [word for word in token_words if not word in start_words]
    print(token_words)
    
    with open('outfile', 'wb') as fp:
        pickle.dump(token_words, fp)

    return token_words

qNa = QnAStatus("text")
(fieldID,ques,ans) = qNa.readExcel()
buildBag_list = []
for each in range(0,44):
    buildBag_list.append(ques[each])
    build_bag_of_words_features_filtered(ques[each])



#build_bag_of_words_features_filtered(ques[0]))