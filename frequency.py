import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

import nltk
nltk.download('wordnet')
 
lemmatizer = WordNetLemmatizer()

def lexical_frequency(word):
    rec = pd.read_csv("unigram_freq.csv")
    sum = np.sum(rec["count"])
    rec["count"] = rec["count"] / sum
    rec = rec.set_index("word")
    return float(rec.loc[word].count.values())
    
def repetition(list):
    rep = 0
    _list = [lemmatizer.lemmatize(l) for l in list]
    words_said = set(_list)
    return len(_list) - len(words_said)

def animal_task(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)

def fruit_veg_task(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    
def f_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "f"])
    
def a_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "a"])
    
def action_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = 0
    
    for w in list:
        pos_l = []
        for tmp in wn.synsets(w):
            if tmp.name().split('.')[0] == w:
                pos_l.append(tmp.pos())
        if "v" in pos_l:
            measures["discrepancy"] += 1
    
    return measures

if __name__ == "__main__":
    print(action_words(["do", "play", "eat", "house", "cat"]))
