#!/bin/bash

raw_dir=/data/p289796/corpus/en-sbn/gold-silver
s2s_based_dir=/data/p289796/SBN-data-silver/s2s_based_data
SA_based_dir=/data/p289796/SBN-data-silver/SA_based_data
GCN_based_dir=/data/p289796/SBN-data-silver/GCN_based_data

mkdir -p "${s2s_based_dir}/word-level/"
mkdir -p "${s2s_based_dir}/char-level/"
mkdir -p "${s2s_based_dir}/anonymize-level/"
mkdir -p "${SA_based_dir}/word-level/"
mkdir -p "${SA_based_dir}/bpe-level/"
mkdir -p "${GCN_based_dir}/anonymize-level/"

echo "-----------------------------------(1)--------------------------------------"
echo "Getting tokenized target sentences data for seq2seq models..."
##"Use Moses tokenizer
#cd
#git clone https://github.com/moses-smt/mosesdecoder.git
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < ${raw_dir}/train.txt.raw > ${s2s_based_dir}/word-level/train.txt.raw.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < ${raw_dir}/dev.txt.raw > ${s2s_based_dir}/word-level/dev.txt.raw.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < ${raw_dir}/test.txt.raw > ${s2s_based_dir}/word-level/test.txt.raw.tok -no-escape 
#cd -
python preprocess_target_char.py ${raw_dir}/train.txt.raw ${s2s_based_dir}/char-level/train.txt.raw.char
python preprocess_target_char.py ${raw_dir}/dev.txt.raw ${s2s_based_dir}/char-level/dev.txt.raw.char
python preprocess_target_char.py ${raw_dir}/test.txt.raw ${s2s_based_dir}/char-level/test.txt.raw.char

##-------------------------------------------------------------------------
echo "First: Getting the data for seq2seq2 models "
## "Getting Word-level and Char-level source SBN data"
python preprocess_s2s.py ${raw_dir}/train.txt ${s2s_based_dir}/word-level/train.txt.word ${s2s_based_dir}/char-level/train.txt.char
python preprocess_s2s.py ${raw_dir}/dev.txt ${s2s_based_dir}/word-level/dev.txt.word ${s2s_based_dir}/char-level/dev.txt.char
python preprocess_s2s.py ${raw_dir}/test.txt ${s2s_based_dir}/word-level/test.txt.word ${s2s_based_dir}/char-level/test.txt.char

echo "-------------------------------------(2)------------------------------------"
echo "Getting tokenized target sentences data for SA-Transformer models..."
## copy the tokenized sentence data to SA-Transformer-based data file
cp ${s2s_based_dir}/word-level/train.txt.raw.tok ${SA_based_dir}/word-level/train.txt.raw.tok
cp ${s2s_based_dir}/word-level/dev.txt.raw.tok ${SA_based_dir}/word-level/dev.txt.raw.tok
cp ${s2s_based_dir}/word-level/test.txt.raw.tok ${SA_based_dir}/word-level/test.txt.raw.tok

##-------------------------------------------------------------------------
echo "Giving the name of all the data need to get ..."
train_sent=${SA_based_dir}/word-level/train.txt.raw.tok
train_sent_bpe=${SA_based_dir}/bpe-level/train.txt.raw.bpe
dev_sent=${SA_based_dir}/word-level/dev.txt.raw.tok
dev_sent_bpe=${SA_based_dir}/bpe-level/dev.txt.raw.bpe
test_sent=${SA_based_dir}/word-level/test.txt.raw.tok
test_sent_bpe=${SA_based_dir}/bpe-level/test.txt.raw.bpe

### get bpe sbn data and sentence data for seq2seq model
cp $s2s_based_dir/word-level/train.txt.word $SA_based_dir/word-level/train.txt.word
train_sbn=$SA_based_dir/word-level/train.txt.word
train_sbn_bpe=$SA_based_dir/bpe-level/train.txt.bpe
cp $s2s_based_dir/word-level/dev.txt.word $SA_based_dir/word-level/dev.txt.word
dev_sbn=$SA_based_dir/word-level/dev.txt.word
dev_sbn_bpe=$SA_based_dir/bpe-level/dev.txt.bpe
cp $s2s_based_dir/word-level/test.txt.word $SA_based_dir/word-level/test.txt.word
test_sbn=$SA_based_dir/word-level/test.txt.word
test_sbn_bpe=$SA_based_dir/bpe-level/test.txt.bpe

### get concept data for SA-Transformer model
train_concept=$SA_based_dir/word-level/train.txt.concept
train_concept_bpe=$SA_based_dir/bpe-level/train.txt.concept_bpe
train_concept_path=$SA_based_dir/word-level/train.txt.concept_path
train_concept_bpe_path=$SA_based_dir/bpe-level/train.txt.concept_bpe_path

dev_concept=$SA_based_dir/word-level/dev.txt.concept
dev_concept_bpe=$SA_based_dir/bpe-level/dev.txt.concept_bpe
dev_concept_path=$SA_based_dir/word-level/dev.txt.concept_path
dev_concept_bpe_path=$SA_based_dir/bpe-level/dev.txt.concept_bpe_path

test_concept=$SA_based_dir/word-level/test.txt.concept
test_concept_bpe=$SA_based_dir/bpe-level/test.txt.concept_bpe
test_concept_path=$SA_based_dir/word-level/test.txt.concept_path
test_concept_bpe_path=$SA_based_dir/bpe-level/test.txt.concept_bpe_path

### get path data
#python preprocess_concept.py $raw_dir/train.txt $train_concept $train_concept_path
#python preprocess_concept.py $raw_dir/dev.txt $dev_concept $dev_concept_path
#python preprocess_concept.py $raw_dir/test.txt $test_concept $test_concept_path

echo "Start learning BPE ..."
#git clone https://github.com/rsennrich/subword-nmt.git
## or ##
## pip install subword-nmt
num_operations=10000
freq=0
codes_file=$SA_based_dir/bpe-level/train.codes
vocab_concept=$SA_based_dir/bpe-level/vocab.concept
vocab_sent=$SA_based_dir/bpe-level/vocab.tok.sent

subword-nmt learn-joint-bpe-and-vocab --input $train_concept $train_sent -s $num_operations -o $codes_file --write-vocabulary $vocab_concept $vocab_sent

subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $train_sbn > $train_sbn_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $train_concept > $train_concept_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $train_sent > $train_sent_bpe

subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $dev_sbn > $dev_sbn_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $dev_concept > $dev_concept_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $dev_sent > $dev_sent_bpe

subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq  < $test_sbn > $test_sbn_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq  < $test_concept > $test_concept_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $test_sent > $test_sent_bpe

#-------------------------------------------------------------------------
echo "Start generating Label paths ..."

#python preprocess_concept_bpe.py $raw_dir/train.txt $train_concept_bpe $train_concept_bpe_path
#python preprocess_concept_bpe.py $raw_dir/dev.txt $dev_concept_bpe $dev_concept_bpe_path
#python preprocess_concept_bpe.py $raw_dir/test.txt $train_concept_bpe $test_concept_bpe_path

echo "-------------------------------------(3)------------------------------------"
echo "Getting tokenized target sentences data for Gragh neural models..."
## copy the tokenized sentence data to SA-Transformer-based data file
cp $s2s_based_dir/word-level/train.txt.raw.tok $GCN_based_dir/train.txt.raw.tok
cp $s2s_based_dir/word-level/dev.txt.raw.tok $GCN_based_dir/dev.txt.raw.tok
cp $s2s_based_dir/word-level/test.txt.raw.tok $GCN_based_dir/test.txt.raw.tok

cp $s2s_based_dir/char-level/train.txt.raw.char $GCN_based_dir/train.txt.raw.char
cp $s2s_based_dir/char-level/dev.txt.raw.char $GCN_based_dir/dev.txt.raw.char
cp $s2s_based_dir/char-level/test.txt.raw.char $GCN_based_dir/test.txt.raw.char

python preprocess_gragh.py $raw_dir/train.txt $GCN_based_dir/train.txt.seq
python preprocess_gragh.py $raw_dir/dev.txt $GCN_based_dir/dev.txt.seq
python preprocess_gragh.py $raw_dir/test.txt $GCN_based_dir/test.txt.seq

echo "-------------------------------------(4)------------------------------------"
echo "Getting Anonymized SBN data and sentence data for Seq2Seq model"
### seq2seq model: anonymized sbn
python preprocess_anonymize_s2s.py $raw_dir/train.txt $raw_dir/train.txt.raw  $s2s_based_dir/anonymize-level/train.txt.anony $s2s_based_dir/anonymize-level/train.txt.raw.anony $s2s_based_dir/anonymize-level/train.alignment
python preprocess_anonymize_s2s.py $raw_dir/dev.txt $raw_dir/dev.txt.raw  $s2s_based_dir/anonymize-level/dev.txt.anony $s2s_based_dir/anonymize-level/dev.txt.raw.anony $s2s_based_dir/anonymize-level/dev.alignment
python preprocess_anonymize_s2s.py $raw_dir/test.txt $raw_dir/test.txt.raw  $s2s_based_dir/anonymize-level/test.txt.anony $s2s_based_dir/anonymize-level/test.txt.raw.anony $s2s_based_dir/anonymize-level/test.alignment

~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $s2s_based_dir/anonymize-level/train.txt.raw.anony > $s2s_based_dir/anonymize-level/train.txt.raw.anony.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $s2s_based_dir/anonymize-level/dev.txt.raw.anony > $s2s_based_dir/anonymize-level/dev.txt.raw.anony.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $s2s_based_dir/anonymize-level/test.txt.raw.anony > $s2s_based_dir/anonymize-level/test.txt.raw.anony.tok -no-escape 

echo "-------------------------------------(5)------------------------------------"
echo "Getting Anonymized SBN data and sentence data for graph neural model"
### graph model: anonymized sbn
python preprocess_anonymize_graph.py $raw_dir/train.txt $raw_dir/train.txt.raw  $GCN_based_dir/anonymize-level/train.txt.seq.anony $GCN_based_dir/anonymize-level/train.txt.raw.anony $GCN_based_dir/anonymize-level/train.alignment
python preprocess_anonymize_graph.py $raw_dir/dev.txt $raw_dir/dev.txt.raw  $GCN_based_dir/anonymize-level/dev.txt.seq.anony $GCN_based_dir/anonymize-level/dev.txt.raw.anony $GCN_based_dir/anonymize-level/dev.alignment
python preprocess_anonymize_graph.py $raw_dir/test.txt $raw_dir/test.txt.raw  $GCN_based_dir/anonymize-level/test.txt.seq.anony $GCN_based_dir/anonymize-level/test.txt.raw.anony $GCN_based_dir/anonymize-level/test.alignment

~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $GCN_based_dir/anonymize-level/train.txt.raw.anony > $GCN_based_dir/anonymize-level/train.txt.raw.anony.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $GCN_based_dir/anonymize-level/dev.txt.raw.anony > $GCN_based_dir/anonymize-level/dev.txt.raw.anony.tok -no-escape 
~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < $GCN_based_dir/anonymize-level/test.txt.raw.anony > $GCN_based_dir/anonymize-level/test.txt.raw.anony.tok -no-escape 

echo "-------------------------------------END------------------------------------"

