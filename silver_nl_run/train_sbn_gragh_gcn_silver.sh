#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --time=5:00:00
#SBATCH --mem=100GB

GPUIDS="${1:-0}"
DATA_DIR="${2:-/data/p289796/SBN-data-silver/nl/sbn-nl-reent}"
OUT_DIR="${3:-/data/p289796/SBN-data-silver/nl/sbn_gcn}"
BATCH_SIZE="${4:-32}"
NUM_LAYERS="${5:-1}"

mkdir -p ${OUT_DIR}

python ../train.py \
    -activation 'relu' \
    -highway 'tanh' \
    -n_gcn_layer 2 \
    -gcn_edge_dropout 0.1 \
    -gcn_dropout 0.1 \
    -data_type 'SBN' \
    -data ${DATA_DIR}/sbn \
    -save_model ${OUT_DIR}/sbn-model \
    -layers ${NUM_LAYERS} \
    -report_every 1000 \
    -train_steps 30001 \
    -valid_steps 3000 \
    -rnn_size 750 \
    -word_vec_size 750 \
    -gcn_vec_size 750 \
    -encoder_type gcn \
    -decoder_type rnn \
    -batch_size ${BATCH_SIZE} \
    -max_generator_batches 50 \
    -save_checkpoint_steps 5000 \
    -decay_steps 1000 \
    -optim sgd \
    -max_grad_norm 3 \
    -learning_rate_decay 0.8 \
    -start_decay_steps 10000 \
    -learning_rate 1 \
    -dropout 0.5 \
    -gpu_ranks ${GPUIDS} \
    -seed 123\
    -keep_checkpoint 3\
    -copy_attn 
  
