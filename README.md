# DRG-generation-Dutch
This repository shows the work for poster " [Comparing Neural Meaning-to-Text Approaches for Dutch"](https://github.com/wangchunliu/DRG-generation-Dutch/blob/main/poster_for_CLIN.pdf) " in CLIN 2022 conference, the sister repository is [here](https://github.com/wangchunliu/DRG-generation-Dutch2).


### INTRODUCTION

- 1. preprocess the sequentail DRG data to graph format 
- 2. compare GCN model with LSTM model
- 3. stacking LSTM with GCN model

### DATA
All the data preprocess we move to this folder " [SBN-Process](https://github.com/wangchunliu/SBN-Process) ".

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

