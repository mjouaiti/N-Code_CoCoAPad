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
    
    return float(rec.loc[word]["count"])
    
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
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))


def fruit_veg_task(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    
def f_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "f"])
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    
def a_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "a"])
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    
def action_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = 0
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    
    for w in list:
        print(w)
        pos_l = []
        print(wn.synsets(w))
        for tmp in wn.synsets(w):
            if tmp.name().split('.')[0] == w:
                pos_l.append(tmp.pos())
        print(pos_l)
        if not "v" in pos_l:
            measures["discrepancy"] += 1
    
    return measures

if __name__ == "__main__":
#    print(action_words(["do", "play", "eat", "house", "dog"]))
    f = open("animal_groups.txt", "r")
    for line in f:
        print(line)
        split = line.split(":")
        cat, words = split[0], split[1].split(",")
        
        print(cat, words)
        
