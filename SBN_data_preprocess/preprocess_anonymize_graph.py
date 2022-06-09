#output is anonymize-level sbn data and replace_alignment file
import sys
import re
import json
from sbn_utils import get_sbn, sbn_string_to_list, between_quotes, list_to_file, file_to_list

def get_anonymize(new_clauses):
    return_strings = []
    alignment = {}
    for index_clause, cur_clause in enumerate(new_clauses):
        for idx, item in enumerate(cur_clause):
            if cur_clause[idx - 1] == 'Name' and between_quotes(cur_clause[idx]):
                cur_clause[idx] = "NAMEname" + str(index_clause)
                #cur_clause[idx] = "NAMEname"
                ### for alignment output file
                alignment[cur_clause[idx]] = item.strip('"') ###(1)
            #if cur_clause[idx - 1] == 'Quantity' and not re.search("\+", cur_clause[idx]) and not re.search("\-", cur_clause[idx]):
                #cur_clause[idx] = "QUANTITYquantity" + str(index_clause)
                ### for alignment output file
                #alignment[cur_clause[idx]] = item.strip('"') ###(2)
            if cur_clause[idx - 1] == 'Name' and cur_clause[idx].startswith('"') and not cur_clause[idx].endswith('"'):
                cur_name = []
                for j in range(idx+1, len(cur_clause), 1):
                    if cur_clause[j].endswith('"'):
                        end_index = j
                        for index in range(idx, end_index+1):
                            cur_name.append(cur_clause[index].strip('"'))
                ### for alignment output file
                #cur_clause[idx] = "NAMEname"
                cur_clause[idx] = "NAMEname" + str(index_clause)
                alignment[cur_clause[idx]] = ' '.join(cur_name) ###(3)
                del cur_clause[idx+1: end_index+1]
        return_strings.append(' '.join(cur_clause))
        return_strings.append('***')
    return return_strings, alignment


if __name__ == "__main__":
    ## input1 is sbn file, -----input2 is sentence file (tok file)
    ## output1 is anonymized sbn, output3 is alignmented file, -----output 2 is anonymized sentence data,.
    input_f1 = sys.argv[1] #sbn file
    input_f2 = sys.argv[2] #token file
    output_f1, output_f2, output_f3  = sys.argv[3], sys.argv[4], sys.argv[5]
    ### get sentence list
    sen_list = file_to_list(input_f2)
    ### get anonymized sbn data
    sbns = get_sbn(input_f1)
    with open(output_f1, 'w') as outfile1, open(output_f2, 'w') as outfile2, open(output_f3, 'w') as outfile3:
        for i, sbn in enumerate(sbns):
            sbn = sbn_string_to_list(sbn)
            sbn_list_word, alignment = get_anonymize(sbn)
            ### get the anonymized sbn file
            outfile1.write(' '.join(sbn_list_word) + '\n')
            ### get the anonymized sentence file
            sen = sen_list[i]
            for key, value in alignment.items():
                try: # two methods to get anonymized sentences
                    sen = re.sub(value, key, sen)
                except:
                    sen = sen.replace(value, key)
            outfile2.write(sen + '\n')
            ### get the dictionary of name entities
            all_align = []
            for key, value in alignment.items():
                all_align.append(key + '|||' + value)
            outfile3.write(' *** '.join(all_align) + '\n')

