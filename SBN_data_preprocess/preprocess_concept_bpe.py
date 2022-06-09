# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from sbn_utils import read_sbn_file, apply_bpe_edge, create_structural_path

if __name__ =='__main__':

    train_file, concept_bpe, path_out = sys.argv[1], sys.argv[2], sys.argv[3]

    file_lst, content_lst = [], []
    for i in range(1, 9):  # Eight paths
        f = open(path_out + '_{}'.format(i), 'w')
        content_lst.append([])
        file_lst.append(f)

    path_out = open(path_out, "w")
    all_instances, max_node_num, max_in_neigh_num, max_out_neigh_num = read_sbn_file(train_file)
    all_paths, all_nodes = [], []
    bpe_f = open(concept_bpe, 'r')
    index = 0
    for amr_data, bpe_line in zip(all_instances, bpe_f):
        index += 1
        nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices, out_neigh_edges = amr_data
        # print('======================{}========================='.format(index))
        # print(nodes)
        # print(in_neigh_indices)
        # print(in_neigh_edges)
        # print(out_neigh_indices)
        # print(out_neigh_edges)

        bpe_nodes = bpe_line.strip().split()
        G1, tag1, G2, tag2 = apply_bpe_edge(bpe_nodes, nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices,
                                            out_neigh_edges)
        # print(bpe_nodes)
        # print(G1)
        # print(tag1)
        # print(G2)
        # print(tag2)
        bpe_path = create_structural_path(G1, G2, tag2)
        # print(bpe_path)
        bpe_nodes.append('EOS')

        lineth_path = []
        kth_path = [[] for _ in range(8)]
        for i in range(len(bpe_nodes)):
            for j in range(len(bpe_nodes)):
                # print("{}->{}\t{}".format(bpe_nodes[i], bpe_nodes[j], bpe_path[(i,j)]))
                lineth_path.append(''.join(bpe_path[(i, j)]))
                for k in range(8):
                    label = bpe_path[(i, j)][k] if k < len(bpe_path[(i, j)]) else '<blank>'
                    kth_path[k].append(label)

        #print(lineth_path)
        all_paths.append(' '.join(lineth_path) + ' ')

        for m in range(8):
            content_lst[m].append(' '.join(kth_path[m]) + ' ')
        # bpe_nodes.pop()
        # all_nodes.append(' '.join(bpe_nodes))
    path_out.write('\n'.join(all_paths))
    for idx, ff in enumerate(file_lst):
        ff.write('\n'.join(content_lst[idx]))

