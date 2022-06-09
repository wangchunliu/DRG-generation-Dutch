# coding-utf-8
'''Used for getting seq2seq data of sbn for gragh model'''
import re
import sys
from sbn_utils import get_sbn, sbn_string_to_list


if __name__ == "__main__":
    # raw sbn data, seq2seq sbn data
    input_f, output_f = sys.argv[1], sys.argv[2]
    sbns = get_sbn(input_f)
    with open(output_f, 'w') as outfile1:
        for i, sbn in enumerate(sbns):
            sbn = sbn_string_to_list(sbn)
            finish_list = []
            for cur_sbn in sbn:
                new_list = ' '.join(cur_sbn)
                finish_list.append(new_list)
                finish_list.append('***')
            outfile1.write(' '.join(finish_list)+'\n')
