"""
Different from 1_split_sbn_data.py,
this script is used to get 100 active/passive examples + 900 normal examples development set,
100 active/passive examples test set.
we also need to distinguish active voice and passive voice
"""

import argparse
import re
import random
import logging as log
from sbn_utils import get_dir_sen, get_dir_sbn, sbn_string_to_list, is_number

def create_arg_parser():
    '''Create argument parser'''
    parser = argparse.ArgumentParser()
    # Parameter that are import to set
    parser.add_argument('-i', "--input", default='', type=str, help="SBN input-file")
    parser.add_argument('-ipath', "--inputpath", default='', type=str, help="SBN input-file path")
    parser.add_argument("-o1", "--output1", default='', type=str, help="gold train")
    parser.add_argument('-o2', "--output2", default='', type=str, help="gold dev")
    parser.add_argument('-o3', "--output3", default='', type=str, help="gold test")
    args = parser.parse_args()
    return args

def get_raw_sbn(f):
    '''Read and return individual sbns in clause format'''
    cur_sbn = []
    all_sbns = []
    for line in open(f, 'r'):
        if not line.strip():
            if cur_sbn:
                all_sbns.append(cur_sbn)
                cur_sbn = []
        else:
            cur_sbn.append(line.strip())
    ## If we do not end with a newline we should add the sbn still
    if cur_sbn:
        all_sbns.append(cur_sbn)
    return all_sbns

def is_active(sbn):
    sbn = sbn_string_to_list(sbn)
    role_list = ['Time', 'Agent', 'Patient']
    verb_role_list = ['Agent']
    for cur_sbn in sbn:
        if set(role_list) < set(cur_sbn):
            for j in range(0, len(cur_sbn) - 2, 2):
                if cur_sbn[j + 1] in verb_role_list and is_number(cur_sbn[j + 2]) and re.search("\-", cur_sbn[j + 2]):
                    return True
    return False

def is_passive(sbn):
    sbn = sbn_string_to_list(sbn)
    role_list = ['Time', 'Agent', 'Patient']
    verb_role_list = ['Agent']
    for cur_sbn in sbn:
        if set(role_list) < set(cur_sbn):
            for j in range(0, len(cur_sbn) - 2, 2):
                if cur_sbn[j + 1] in verb_role_list and is_number(cur_sbn[j + 2]) and re.search("\+", cur_sbn[j + 2]):
                    return True
    return False
## TEST: 50 active voice instances and 50 passive voice instances
## DEV: 50 active voice instances and 50 passive voice instances + 900 normal instances
## TRAIN: other data in gold data
def split_active_sbn(inputfile):
    sbns = get_raw_sbn(inputfile)
    active_dir = []
    passive_dir = []
    normal_dir = []
    for index, sbn in enumerate(sbns):
        
        path = re.search('p\d{2}/d\d{4}', sbn[1])
        if is_active(sbn):
            active_dir.append(path.group(0))
        elif is_passive(sbn):
            passive_dir.append(path.group(0))
        else:
            normal_dir.append(path.group(0))
    ## random spilt them to different set
    random.shuffle(active_dir)
    random.shuffle(passive_dir)
    random.shuffle(normal_dir)
    print(len(active_dir))
    print(len(passive_dir))
    print(len(normal_dir))
    test_data_dir = active_dir[:80] + passive_dir[:20]
    dev_data_dir = active_dir[80:160] + passive_dir[20:40] + normal_dir[:900]
    train_data_dir = active_dir[160:] + passive_dir[40:] + normal_dir[900:]
    return train_data_dir, dev_data_dir, test_data_dir


if __name__ == "__main__":
    # all gold data, input data and input path
    # output is train data, dev data and test data
    args = create_arg_parser()
    print("get all the data path")
    train_data_dir, dev_data_dir, test_data_dir = split_active_sbn(args.input)
    print("get all the raw sbn data")
    get_dir_sbn(args.inputpath, train_data_dir, args.output1)
    get_dir_sbn(args.inputpath, dev_data_dir, args.output2)
    get_dir_sbn(args.inputpath, test_data_dir, args.output3)
    print("get all the raw sentences data")
    get_dir_sen(args.inputpath, train_data_dir, args.output1 + '.raw')
    get_dir_sen(args.inputpath, dev_data_dir, args.output2 + '.raw')
    get_dir_sen(args.inputpath, test_data_dir, args.output3 + '.raw')
    print("done")
