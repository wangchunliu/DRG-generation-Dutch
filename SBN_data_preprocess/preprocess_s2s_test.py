'''
idea：replace unkown concepts in test data with hypernmy wordnet in training data
pipeline:
1. get all the concepts in training data
2. check whether a concepts in training data, if not, get its hyper or similar, check whether in training data,
if not, increase path distance
'''
import sys
import re
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
    try: # concept should be a right format of Wordnet
        wordnet_nltk = wn.synset(test_concept) # adjective wordnet can use similarity
        print("Curent unknown wordnet: {0}".format(test_concept))
        # 3. 下义词
        all_hyponyms_wordnet = list(set([i for i in wordnet_nltk.closure(lambda s: s.hyponyms())]))
        if len(all_hyponyms_wordnet)>0:
            try:
                for hyponyms_wordnet in all_hyponyms_wordnet:
                    if str(hyponyms_wordnet)[8:-2] in train_concept:
                        similarity = wordnet_nltk.path_similarity(hyponyms_wordnet)
                        if float(similarity) > float(mostsimilarity_hypo):
                            mostsimilarity_hypo = similarity
                            similar_wordnet = str(hyponyms_wordnet)[8:-2]
                return similar_wordnet
            except:
                print(('No hyponnmy in training data: {0}'.format(test_concept)))
        # 2. 上义词
        all_hypernyms_wordnet = list(set([i for i in wordnet_nltk.closure(lambda s: s.hypernyms())]))
        if len(all_hypernyms_wordnet)>0:
            try:
                for hypernyms_wordnet in all_hypernyms_wordnet:
                    if str(hypernyms_wordnet)[8:-2] in train_concept:
                        similarity = wordnet_nltk.path_similarity(hypernyms_wordnet)
                        if float(similarity) > float(mostsimilarity_hyper):
                            mostsimilarity_hyper = similarity
                            similar_wordnet = str(hypernyms_wordnet)[8:-2]
                return similar_wordnet
            except:
                print(('No hypernmy in training data: {0}'.format(test_concept)))
        # 1. 相似词
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
    except:
        print('Wordnet Error:{0}'.format(test_concept))
    return test_concept


def find_similar_as(test_concept, train_concept):
    try: # concept should be a right format of Wordnet
        wordnet_nltk = wn.synset(test_concept) # adjective wordnet can use similarity
        print("Curent unknown wordnet: {0}".format(test_concept))
        # 1. also_sees()
        also_sees_wordnet = wordnet_nltk.also_sees()
        if len(also_sees_wordnet)>0:
            try:
                for see_wordnet in also_sees_wordnet:
                    if str(see_wordnet)[8:-2] in train_concept:
                        return str(see_wordnet)[8:-2]
            except:
                print(('No Also_sees in training data: {0}'.format(test_concept)))
        # 2. similar_tos()
        similar_tos_wordnet= wordnet_nltk.similar_tos()
        if len(similar_tos_wordnet)>0:
            try:
                for similar_wordnet in similar_tos_wordnet:
                    if str(similar_wordnet)[8:-2] in train_concept:
                        return str(similar_wordnet)[8:-2]
            except:
                print(('No Similar_tos in training data: {0}'.format(test_concept)))
    except:
        print('Wordnet Error:{0}'.format(test_concept))
    return test_concept

if __name__ == "__main__":
    train_preprocessed_file = sys.argv[1]  ## preprocessed train file
    train_concept_n, train_concept_a, train_concept_v, train_concept_r = get_concept(train_preprocessed_file)  ## vocabulary of concepts
    #----------------------------------
    test_preprocessed_file = sys.argv[2] ## preprocessed test file
    new_test_preprocessed_file = sys.argv[3]
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
                    print(new_concept)
                    print(cur_sbn[0])
                    cur_sbn[0] = new_concept
                if concept_v and cur_sbn[0] not in train_concept_v: #Verb
                    new_concept = find_similar_nv(cur_sbn[0], train_concept_v)
                    print(new_concept)
                    print(cur_sbn[0])
                    cur_sbn[0] = new_concept
                if concept_a and cur_sbn[0] not in train_concept_a: #Adjective
                    new_concept = find_similar_as(cur_sbn[0], train_concept_a)
                    print(new_concept)
                    print(cur_sbn[0])
                    cur_sbn[0] = new_concept
                # if concept_r and cur_sbn[0] not in train_concept_r: # Adverb
                #     new_concept = find_similar_nv(cur_sbn[0], train_concept_r)
                #     print(new_concept)
                #     print(cur_sbn[0])
                #     cur_sbn[0] = new_concept
                finish_list.extend(cur_sbn)
            outfile.write(' '.join(finish_list) + '\n')

