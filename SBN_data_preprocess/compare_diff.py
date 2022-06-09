import sys

def write_to_file(lst, out_file):
    '''Write list to file'''
    with open(out_file, "w") as out_f:
        for line in lst:
            out_f.write(line.strip() + '\n')
    out_f.close()

def write_list_of_lists(lst, out_file, extra_new_line=True):
    '''Write lists of lists to file'''
    with open(out_file, "w") as out_f:
        for i, sub_list in enumerate(lst):
            out_f.write('(' + str(i) + ')' + '\n')
            for item in sub_list:
                out_f.write(item.strip() + '\n') 
            if extra_new_line:
                out_f.write('---'+'\n')
    out_f.close()

def get_list(file):
    list = []
    with open(file, 'r') as input:
        for line in input.readlines():
            list.append(line.strip())
    return list

def compare_diff(file1, file2, file3, outfile):
    list1 = get_list(file1)
    list2 = get_list(file2)
    list3 = get_list(file3)
    list = []
    for i in range(len(list1)):
        cur_list = [list1[i], list2[i], list3[i]]
        list.append(cur_list)
    write_list_of_lists(list, outfile)

if __name__ == '__main__':
    file1, file2, file3, outfile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    compare_diff(file1, file2, file3, outfile)
