#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --time=2:00:00
#SBATCH --mem=100GB


GPUIDS="${1:-0}"
DATA_DIR="${2:-/data/p289796/SBN-data-silver/nl/sbn-nl}"
OUT_DIR="${3:-/data/p289796/SBN-data-silver/nl/sbn_seq}"
BATCH_SIZE="${4:-32}"
NUM_LAYERS="${5:-1}"

mkdir -p ${OUT_DIR}

python ../train.py \
    -data_type 'text' \
    -data ${DATA_DIR}/sbn \
    -save_model ${OUT_DIR}/sbn-model \
    -layers ${NUM_LAYERS} \
    -report_every 1000 \
    -train_steps 30001 \
    -valid_steps 3000 \
    -rnn_size 900 \
    -word_vec_size 450 \
    -encoder_type brnn \
    -decoder_type rnn \
    -batch_size ${BATCH_SIZE} \
    -max_generator_batches 50 \
    -learning_rate_decay 0.8 \
    -start_decay_steps 10000 \
    -save_checkpoint_steps 5000 \
    -decay_steps 1000 \
    -optim sgd \
    -max_grad_norm 3 \
    -learning_rate 1 \
    -seed 123 \
    -dropout 0.5 \
    -keep_checkpoint 3\
    -gpu_ranks ${GPUIDS} \
    -copy_attn 
