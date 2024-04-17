import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

#import nltk
#nltk.download('wordnet')
 
lemmatizer = WordNetLemmatizer()

def lexical_frequency(word):
    rec = pd.read_csv("unigram_freq.csv")
    sum = np.sum(rec["count"])
    rec["count"] = rec["count"] / sum
    rec = rec.set_index("word")
    
    return float(rec.loc[word]["count"])
    
def repetition(list_):
    rep = 0
    _list = [lemmatizer.lemmatize(l) for l in list_]
    words_said = set(_list)
    return len(_list) - len(words_said)
    
from itertools import groupby
def switching_clustering(list_, word_dict):
    cat = []
    for l in list_:
        try:
            cat.append(word_dict[l])
        except:
            cat.append(["NA"])
            
    # clustering
    inter = []
    for i in range(len(cat) - 1):
        c1, c2 = cat[i], cat[i + 1]
        intersection = list(set(c1) & set(c2))
        try:
            inter.append(intersection[0])
        except:
            inter.append("")
    
    res = []
    for k, g in groupby(inter):
        res.extend([k, str(len(list(g)))])
    
        
    nb_clusters = 0
    for k in range(0, len(res) - 1, 2):
        c_name = res[k]
        c_size = res[k + 1]
        if c_name == "":
            nb_clusters += int(c_size)
        else:
            nb_clusters += 1
            
    if res[0] == "" and len(res) == 2:
        nb_clusters = len(cat)
    nb_switches = nb_clusters - 1
    
    return nb_clusters, nb_switches, res
    
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

def animal_task(list_):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list_]
    measures["repetition"] = repetition(list_)
    measures["word_count"] = len(list_)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list_]))
    measures["discrepancy"] = len([w for w in list_ if w not in animal_dict])
    measures["nb_clusters"], measures["nb_switches"], measures["clusters"] = switching_clustering(list_, animal_dict)
    
    return measures


def fruit_veg_task(list_):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list_]
    measures["repetition"] = repetition(list_)
    measures["word_count"] = len(list_)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list_]))
    measures["fruit_veg_categories"] = switching_clustering(list_, fruit_dict)
    measures["discrepancy"] = len([w for w in list_ if w not in fruit_dict])
    measures["nb_clusters"], measures["nb_switches"] = switching_clustering(list_)
    
    
def f_starting_words(list_):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list_]
    measures["repetition"] = repetition(list_)
    measures["discrepancy"] = len([word for word in list_ if not word[0].lower() == "f"])
    measures["word_count"] = len(list_)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list_]))
    measures["nb_clusters"], measures["nb_switches"] = switching_clustering(list_)
    
    return measures
    
def a_starting_words(list_):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list_]
    measures["repetition"] = repetition(list_)
    measures["discrepancy"] = len([word for word in list_ if not word[0].lower() == "a"])
    measures["word_count"] = len(list_)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list_]))
    measures["nb_clusters"], measures["nb_switches"] = switching_clustering(list_)
    
    return measures

    
def action_words(list_):
    measures = {}
    # discrepancy/asides
    measures["lexical_frequency"] = [lexical_frequency(word) for word in list_]
    measures["repetition"] = repetition(list_)
    measures["discrepancy"] = 0
    measures["word_count"] = len(list_)
    measures["unique_word_count"] = len(set([lemmatizer.lemmatize(l) for l in list_]))
    measures["nb_clusters"], measures["nb_switches"] = switching_clustering(list_)
    
    
    for w in list_:
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

    list_ = ["cat", "dog", "wolf", "parrot", "dog", "hamster", "tuna", "camel", "play"]
    list_ = ["dog", "lion", "fish"]
    list_ = ["dog", "cat"]
        
    list_ = [l.lower() for l in list_]
#    Walk, crawl, jump. Leap. Gallop, stroll. Enter. Exercise. size.'
#father_animals.wav
#'text':
#father_A_words.wav
#'text': ' Artfork, Apple, S, Ores, Endla, Abacus, Artifact Albium Acorn Aster Asva. Adornment.''

    text = 'Fox, horse, rabbit, snake, whale, crab, person, giraffe, hyena, tortoise, meerkat, tiger, bison, cow, horse, sheep, goat, chicken, cat, dog, seal, sea lion, shark, dogfish.'
    
    text = text.lower().replace(",", "").replace(".", "").split(" ")
    
    print(animal_task(text))

