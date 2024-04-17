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
    
def switching_clustering(list, word_dict):
    cat = []
    for l in list:
        cat.append(word_dict[l])
    
    return cat
    
def generate_animal_dict():

    f = open("animal_groups.txt", "r")
    animal_dict = {}
    
    for line in f:
        split = line.split(":")
        cat, words = split[0], split[1].split(",")
        words = [w.strip() for w in words]
        
        for w in words:
            if w in animal_dict:
                animal_dict[w].append(cat)
            else:
                animal_dict[w] = [cat]

    return animal_dict

animal_dict = generate_animal_dict()

def animal_task(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    measures["animal_categories"] = switching_clustering(list, animal_dict)
    
    return measures


def fruit_veg_task(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    measures["animal_categories"] = switching_clustering(list, fruit_dict)
    
def f_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "f"])
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    return measures
    
def a_starting_words(list):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list]
    measures["repetition"] = repetition(list)
    measures["discrepancy"] = np.count([word for word in list if not word[0].lower() == "a"])
    measures["word_count"] = len(list)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list]))
    return measures

    
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

    list = ["cat", "dog", "parrot", "dog", "tuna", "camel"]
    list = [l.lower() for l in list]
    
    print(animal_task(list))

