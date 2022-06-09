import argparse
import re
import os
import logging as log

def create_arg_parser():
    '''Create argument parser'''
    parser = argparse.ArgumentParser()
    # Parameter that are import to set
    parser.add_argument('-i', "--input", default='', type=str, help="SBN input-file")
    parser.add_argument('-ipath', "--inputpath", default='', type=str, help="SBN input-file path")
    parser.add_argument('-o', "--output", default='', type=str, help="SBN output-file")
    args = parser.parse_args()
    return args

## Get pXX/dXXXX by drs document(train.txt)
def specific_dirs(filename):
    '''Read list of pXX/dXXXX from the file and return them'''
    dir_list = []
    if not filename:
        return set(dir_list)
    with open(filename, 'r') as f:
        for line in f:
            m = re.search('p\d{2}/d\d{4}', line)
            if m:
                dir_list.append(m.group(0))
    return dir_list

def get_list_sbn(f):
    '''Read and return individual sbns in clause format'''
    dir_list = []
    cur_sbn = []
    all_sbns = []
    for line in open(f, 'r'):
        if not line.strip():
            if cur_sbn:
                all_sbns.append(cur_sbn)
                cur_sbn = []
        else:
            cur_sbn.append(line.strip())
    ## If we do not end with a newline we should add the sbn still
    if cur_sbn:
        all_sbns.append(cur_sbn)
    for sbn in all_sbns:
        if len(sbn) > 2:
            m = re.search('p\d{2}/d\d{4}', sbn[1])
            dir_list.append(m.group(0))
    return dir_list

def get_dir_sen(inputpath, sen_dir, outfile):
    with open(outfile,'w') as out_f:
        for line in sen_dir:
            raw_path = os.path.join(inputpath, "{}/en.raw".format(line.strip()))
            with open(raw_path, 'r') as raw_f:
                size = os.path.getsize(raw_path)
                if size != 0:
                    a = ''
                    sentences = raw_f.readlines()
                    for sentence in sentences:
                        a += sentence.strip()+' '
                    out_f.writelines(a + '\n')
                else:
                    log.info("The raw sentence file {} does not exist".format(raw_path))
    return out_f

def get_dir_sbn(inputpath, sbn_dir, outfile):
    content = []
    with open(outfile,'w') as out_f:
        for line in sbn_dir:
            sbn_path = os.path.join(inputpath, "{}/en.drs.sbn".format(line.strip()))
            with open(sbn_path, 'r') as sbn_f:
                content = sbn_f.readlines()
                out_f.writelines(content)
                out_f.writelines('\n')


if __name__ == "__main__":
    args = create_arg_parser()
    outdir = get_list_sbn(args.input)
    get_dir_sbn(args.inputpath, outdir, args.output)
    get_dir_sen(args.inputpath, outdir, args.output + '.raw')
