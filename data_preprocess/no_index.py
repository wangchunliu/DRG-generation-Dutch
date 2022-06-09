import sys
import re
def is_number(n):
    try:
        num = float(n)
        # 检查 "nan"
        is_number = num == num  # 或者使用 `math.isnan(num)`
    except ValueError:
        is_number = False
    return is_number

def delete_index(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            list = []
            line_list = line.split()
            for item in line_list:
                if is_number(item) and (re.search("\-", item) or re.search("\+", item)):
                    continue
                else:
                    list.append(item)
            new_line = ' '.join(list)
            outfile.write(new_line + '\n')

input = sys.argv[1]
output = sys.argv[2]
delete_index(input, output)
