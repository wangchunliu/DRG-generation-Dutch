#!/bin/bash


OUT_DIR=/data/p289796/SBN-data-silver/nl/"${1:-sbn-nl-reent}"
DATA_DIR=/data/p289796/corpus/en-sbn/multi-data/nl/gold-silver-bronze
mkdir -p ${OUT_DIR}


python ../preprocess.py \
    -seed 123 \
    -reentrancies \
    -data_type SBN \
    -train_src ${DATA_DIR}/train.txt.graph.normal  \
    -train_tgt ${DATA_DIR}/train.txt.raw \
    -valid_src ${DATA_DIR}/dev.txt.graph.normal \
    -valid_tgt ${DATA_DIR}/dev.txt.raw \
    -save_data ${OUT_DIR}/sbn \
    -src_words_min_frequency 1 \
    -tgt_words_min_frequency 1 \
    -src_seq_length 1000 \
    -tgt_seq_length 1000\
    -dynamic_dict
   
