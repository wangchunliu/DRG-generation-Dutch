#!/bin/bash

GPU_ID="${2:-0}"
DATASET=test

MODELS_DIR="/data/p289796/SBN-data-silver/nl/sbn_gcn"

INPUT_DATA=/data/p289796/corpus/en-sbn/multi-data/nl/gold-silver-bronze
OUT_DIR=${MODELS_DIR}/preds/
MODEL=${MODELS_DIR}/best.pt

REF_FILE=${INPUT_DATA}/${DATASET}.txt.graph.normal
TARG_FILE=${INPUT_DATA}/${DATASET}.txt.raw


mkdir -p ${OUT_DIR}
for fname in ${MODELS_DIR}/*model*; do
    f=${fname##*/}
    echo $f
    python ../translate.py \
	-data_type SBN \
        -model ${fname} \
        -src ${REF_FILE} \
        -tgt ${TARG_FILE} \
        -output ${OUT_DIR}/{$f}.pred.txt \
        -beam_size 5 \
        -batch_size 1 \
        -gpu ${GPU_ID} \
        -replace_unk \
        -max_length 500 > log.txt
done

#python ../postprocess.py -i ${OUT_DIR}/{$f}.pred.txt -o  ${OUT_DIR}/{$f}.pred.txt.tok
#~/mosesdecoder/scripts/tokenizer/detokenizer.perl -l en < ${OUT_DIR}/{$f}.pred.txt.tok > ${OUT_DIR}/{$f}.detok.pred.txt
python ~/project/e2e-metrics/measure_scores.py ${INPUT_DATA}/test.txt.raw ${OUT_DIR}/{$f}.pred.txt


