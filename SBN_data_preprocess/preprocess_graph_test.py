'''
idea：replace unkown concepts in test data with hypernmy wordnet in training data
pipeline:
1. get all the concepts in training data
2. check whether a concepts in training data, if not, get its hyper or similar, check whether in training data,
if not, increase path distance
'''
import sys
import re
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def split_sbn_list(list):
    cur_list = []
    all_list = []
    for i, item in enumerate(list):
        if item == "***":
            all_list.append(cur_list)
            cur_list = []
        else:
            cur_list.append(item.strip())
    return all_list

def get_concept(train_file):
    train_concept_n = []
    train_concept_a = []
    train_concept_v = []
    train_concept_r = []
    with open(train_file, 'r') as sbns:
        for sbn in sbns:
            ### get sequence sbn data from preprocessed sbn data
            sbn_x = sbn.strip().split()
            seq_sbn = split_sbn_list(sbn_x)
            for cur_sbn in seq_sbn:
                # { Part-of-speech constants: ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v" }
                n = re.search(r'\.n\.', cur_sbn[0])
                a = re.search(r'\.a\.|\.s\.', cur_sbn[0])
                v = re.search(r'\.v\.', cur_sbn[0])
                r = re.search(r'\.r\.', cur_sbn[0])
                if n and cur_sbn[0] not in train_concept_n:
                    train_concept_n.append(cur_sbn[0])
                if a and cur_sbn[0] not in train_concept_a:
                    train_concept_a.append(cur_sbn[0])
                if v and cur_sbn[0] not in train_concept_v:
                    train_concept_v.append(cur_sbn[0])
                if r and cur_sbn[0] not in train_concept_r:
                    train_concept_r.append(cur_sbn[0])
        return train_concept_n, train_concept_a, train_concept_v, train_concept_r

def find_similar_nv(test_concept, train_concept):
    mostsimilarity_simi = float(0)
    mostsimilarity_hypo = float(0)
    mostsimilarity_hyper = float(0)
    # concept should be a right format of Wordnet
    print("Curent unknown wordnet: {0}".format(test_concept))
    try:
        wordnet_nltk = wn.synset(test_concept)  # adjective wordnet can use similarity
        if str(wordnet_nltk)[8:-2] in train_concept:
            return str(wordnet_nltk)[8:-2]
    except:
        print('Wordnet Error:{0}'.format(test_concept))
    else:
        # 1. 下义词 2.上义词
        all_hyponyms_wordnet = list(set([i for i in wordnet_nltk.closure(lambda s: s.hyponyms())]))
        all_hypernyms_wordnet = list(set([i for i in wordnet_nltk.closure(lambda s: s.hypernyms())]))
        all_wordnet =  all_hyponyms_wordnet + all_hypernyms_wordnet
        if len(all_wordnet) > 0:
            try:
                for hyperhypo_wordnet in all_wordnet:
                    if str(hyperhypo_wordnet)[8:-2] in train_concept:
                        similarity = wordnet_nltk.path_similarity(hyperhypo_wordnet)
                        if float(similarity) > float(mostsimilarity_hyper):
                            mostsimilarity_hyper = similarity
                            similar_wordnet = str(hyperhypo_wordnet)[8:-2]
                return similar_wordnet
            except:
                print(('No hypernmy and hyponmy in training data: {0}'.format(test_concept)))
        # 3. 相似词
        try:
            for one_concept in train_concept:
                one_wordnet = wn.synset(one_concept)
                similarity = wordnet_nltk.path_similarity(one_wordnet)
                if similarity and float(similarity) > float(mostsimilarity_simi):
                    mostsimilarity_simi = similarity
                    similar_wordnet = one_concept
            return similar_wordnet
        except:
            print(('No similar concept in training data: {0}'.format(test_concept)))
    return test_concept


def find_similar_as(test_concept, train_concept):
    print("Curent unknown wordnet: {0}".format(test_concept))
    try: # concept should be a right format of Wordnet
        wordnet_nltk = wn.synset(test_concept) # adjective wordnet can use similarity
        if str(wordnet_nltk)[8:-2] in train_concept:
            return str(wordnet_nltk)[8:-2]
    except:
        print('Wordnet Error:{0}'.format(test_concept))
    else:
        # 1. also_sees() # 2. similar_tos()
        also_sees_wordnet = wordnet_nltk.also_sees()
        similar_tos_wordnet = wordnet_nltk.similar_tos()
        similar_wordnets = also_sees_wordnet + similar_tos_wordnet
        if len(similar_wordnets)>0:
            try:
                for see_wordnet in similar_wordnets:
                    if str(see_wordnet)[8:-2] in train_concept:
                        return str(see_wordnet)[8:-2]
            except:
                print(('No Similar Wordnets in training data: {0}'.format(test_concept)))
        else:
            print(('No Similar Wordnets: {0}'.format(test_concept)))
    return test_concept

if __name__ == "__main__":
    train_preprocessed_file = sys.argv[1] ## preprocessed train file
    train_concept_n, train_concept_a, train_concept_v, train_concept_r = get_concept(train_preprocessed_file) ## vocabulary of concepts
    #----------------------------------
    test_preprocessed_file = sys.argv[2] ## preprocessed test file
    new_test_preprocessed_file = sys.argv[3]
    concept_noun = open('Unknown.noun.txt','w')
    concept_verb = open('Unknown.verb.txt','w')
    concept_adj = open('Unknown.adj.txt', 'w')
    concept_adv = open('Unknown.adv.txt', 'w')
    with open(test_preprocessed_file, 'r') as raw_test_file, open(new_test_preprocessed_file, 'w') as outfile:
        for line in raw_test_file:
            finish_list = []
            line_x = line.strip().split()
            line = split_sbn_list(line_x)
            for cur_sbn in line:# the first item is WordNet
                concept_n = re.search(r'\.n\.', cur_sbn[0])
                concept_a = re.search(r'\.a\.|\.s\.', cur_sbn[0])
                concept_v = re.search(r'\.v\.', cur_sbn[0])
                concept_r = re.search(r'\.r\.', cur_sbn[0])
                if concept_n and cur_sbn[0] not in train_concept_n: # Noun
                    new_concept = find_similar_nv(cur_sbn[0], train_concept_n)
                    print(cur_sbn[0])
                    print(new_concept)
                    if cur_sbn[0] != new_concept:
                        concept_noun.write(cur_sbn[0] +': '+ new_concept+'\n')
                    cur_sbn[0] = new_concept
                if concept_v and cur_sbn[0] not in train_concept_v: #Verb
                    new_concept = find_similar_nv(cur_sbn[0], train_concept_v)
                    print(cur_sbn[0])
                    print(new_concept)
                    if cur_sbn[0] != new_concept:
                        concept_verb.write(cur_sbn[0] +': '+ new_concept+ '\n')
                    cur_sbn[0] = new_concept
                if concept_a and cur_sbn[0] not in train_concept_a: #Adjective
                    new_concept = find_similar_as(cur_sbn[0], train_concept_a)
                    print(cur_sbn[0])
                    print(new_concept)
                    if cur_sbn[0] != new_concept:
                        concept_adj.write(cur_sbn[0] +': '+ new_concept+'\n')
                    cur_sbn[0] = new_concept
                if concept_r and cur_sbn[0] not in train_concept_r: # Adverb
                    new_concept = find_similar_as(cur_sbn[0], train_concept_r)
                    print(cur_sbn[0])
                    print(new_concept)
                    if cur_sbn[0] != new_concept:
                        concept_adv.write(cur_sbn[0] +': '+ new_concept+'\n')
                    cur_sbn[0] = new_concept
                new_list = ' '.join(cur_sbn)
                finish_list.append(new_list)
                finish_list.append('***')
            outfile.write(' '.join(finish_list) + '\n')

