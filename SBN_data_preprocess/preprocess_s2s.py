# coding-utf-8
'''Used for getting char-level and word-level data for sbn'''
import re
import sys

def get_sbn(f):
    '''Read and return individual sbns in clause format'''
    cur_sbn = []
    all_sbns = []
    for line in open(f, 'r'):
        annotaion = re.search('%%%', line)
        if not line.strip():
            if cur_sbn:
                all_sbns.append(cur_sbn)
                cur_sbn = []
        else:
            if annotaion:
                # delete first three lines comments
                continue
            else:
                cur_sbn.append(line.strip())
    ## If we do not end with a newline we should add the sbn still
    if cur_sbn:
        all_sbns.append(cur_sbn)
    return all_sbns

def sbn_string_to_list(sbn):
    '''Change a sbn in string format (single list) to a list of lists
       Also remove comments from the sbn'''
    sbn = [x for x in sbn if x.strip() and not x.startswith('%')]
    sbn = [x.split('%')[0].strip() for x in sbn]
    sbn = [clause.split()[0:clause.split().index('%')] if '%' in clause.split() else clause.split() for clause in sbn]
    return sbn

def between_quotes(string):
    '''Return true if a value is between quotes'''
    return (string.startswith('"') and  string.endswith('"')) or (string.startswith("'") and string.endswith("'"))

def is_operator(string):
    '''Checks if all items in a string are uppercase'''
    return all(x.isupper() or x.isdigit() for x in string) and string[0].isupper()


def is_role(string):
    '''Check if string is in the format of a role'''
    return string[0].isupper() and any(x.islower() for x in string[1:]) and all(x.islower() or x.isupper() or x == '-' for x in string)


def word_level_sbn(new_clauses):
    '''Return to string format, use char-level for concepts'''
    return_strings = []
    for cur_clause in new_clauses:
        for idx, item in enumerate(cur_clause):
            if cur_clause[idx-1] == 'Name' and between_quotes(cur_clause[idx]):
                cur_clause[idx] = item.strip('"')
            if cur_clause[idx-1] == 'Quantity':
                cur_clause[idx] = item.strip('')
            if cur_clause[idx].startswith('"') and not cur_clause[idx].endswith('"'):
                for j in range(idx, len(cur_clause), 1):
                    if cur_clause[j].endswith('"'):
                        end_index = j
                        for index in range(idx, end_index+1):
                            cur_clause[index] = cur_clause[index].strip('"')
        return_strings.extend(cur_clause)
    return return_strings

def char_level_sbn(new_clauses):
    '''Return to string format, use char-level for concepts'''
    return_strings = []
    for cur_clause in new_clauses:
        for idx, item in enumerate(cur_clause):
            if cur_clause[idx-1] == 'Name' and between_quotes(cur_clause[idx]):
                cur_clause[idx] = " ".join(item.strip('"'))
            if cur_clause[idx-1] == 'Quantity':
                cur_clause[idx] = " ".join(item.strip(''))
            if cur_clause[idx].startswith('"') and not cur_clause[idx].endswith('"'):
                for j in range(idx, len(cur_clause), 1):
                    if cur_clause[j].endswith('"'):
                        end_index = j
                        for index in range(idx, end_index+1):
                            cur_clause[index] = " ".join(cur_clause[index].strip('"'))
        return_strings.extend(cur_clause)
    return return_strings


if __name__ == "__main__":
    # input is sbn file and output is char-level sbn file
    input_f, output_f1, output_f2 = sys.argv[1], sys.argv[2], sys.argv[3]

    sbns = get_sbn(input_f)
    with open(output_f1, 'w') as outfile1:
        for i, sbn in enumerate(sbns):
            sbn = sbn_string_to_list(sbn)
            sbn_list_word = word_level_sbn(sbn)
            outfile1.write(' '.join(sbn_list_word) + '\n')
    with open(output_f2, 'w') as outfile2:
        for i, sbn in enumerate(sbns):
            sbn = sbn_string_to_list(sbn)
            sbn_list_char = char_level_sbn(sbn)
            outfile2.write(' '.join(sbn_list_char) + '\n')



