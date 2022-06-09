# coding-utf-8

import sys

def read_and_strip_file(f):
    '''Read file and strip each line'''
    return [x.strip() for x in open(f, 'r')]

def fix_quotes(sents):
    '''AllenNLP doesn't like sentences with mismatched (unaligned) quotes
           If we encounter such a sentence, just remove the last occurence'''
    new_sents = []
    for sent in sents:
        if sent.count('"') % 2 != 0:
            spl_sent = sent.split('"')
            # Only remove last quote
            final_sent = '"'.join(spl_sent[:-1]) + spl_sent[-1]
            new_sents.append(final_sent)
        else:
            new_sents.append(sent)
    return new_sents

def char_tokenization(in_sents):
    '''Do character-level tokenization, i.e. change:
       Tom loves Mary to T o m + l o v e s + M a r y'''
    # Split tokens to char level and separate tokens by separation character
    sep = '|||'
    sents = [" ".join(" ".join(" ".join(x.split()).replace(' ', sep))
                      .replace(" ".join(sep), sep).split()) for x in in_sents]
    # We have to change back uppercase features that got split into individual characters
    return sents

def write_to_file(lst, out_file):
    '''Write list to file'''
    with open(out_file, "w") as out_f:
        for line in lst:
            out_f.write(line.strip() + '\n')
    out_f.close()

if __name__ == '__main__':
    input_f, output_f = sys.argv[1], sys.argv[2]

    sentences = read_and_strip_file(input_f)
    sents = char_tokenization(sentences)
    sents = fix_quotes(sents)
    write_to_file(sents, output_f)