# DRG-generation-Dutch
This repository shows the work for poster " [Comparing Neural Meaning-to-Text Approaches for Dutch"](https://github.com/wangchunliu/DRG-generation-Dutch/blob/main/poster_for_CLIN.pdf) " in CLIN 2022 conference, the sister repository is [here](https://github.com/wangchunliu/DRG-generation-Dutch2).


### INTRODUCTION

- 1. preprocess the sequentail DRS data to graph format 
- 2. compare GCN model with LSTM model
- 3. stacking LSTM with GCN model

### DATA
All the data preprocess file in the folder " [data_preprocess](https://github.com/wangchunliu/DRG-generation-Dutch/tree/main/data_preprocess) ".
This folder looks very cluttered.
If you want to get the data from scratch, please use the following steps, if there are errors, please tell me.

```
## 1.download data from PMB, for other version data, you can access https://pmb.let.rug.nl/data.php
wget https://pmb.let.rug.nl/releases/pmb-4.0.0.zip

## 2. process data to make different language (en, it, nl, de) and different types (gold, silver, bronze) data in different files.
sh set_up.sh

## 3. preprocess the clause format data to sequential format data for neural models

python ../data_preprocess/sbn_preprocess.py  -input_src ${DATA_DIR}/train.txt -input_tgt ${DATA_DIR}/train.txt.raw -text_type graph -if_anony normal
# or: no *** 
python ../data_preprocess/sbn_preprocess.py  -input_src ${DATA_DIR}/train.txt -input_tgt ${DATA_DIR}/train.txt.raw -text_type seq -if_anony normal
```

### METHODS

#### Step1: Preprocess
```
cd silver_nl_run
sh preproc_sbn_silver.sh ## get date for seq2seq models
sh preproc_sbn_reent_silver.sh ## get data for graph models and stacking models
```
#### Step2: Training 
```
cd silver_nl_run
sh train_sbn_gragh_gcn_silver.sh ## train the gcn model
sh train_sbn_seq_silver.sh ## train the lstm model
```
#### Step3: Predict
```
cd silver_nl_run
sh predict_sbn_reent_silver.sh ## predict the gcn model
sh predict_sbn_silver.sh ## predict the lstm model
```

