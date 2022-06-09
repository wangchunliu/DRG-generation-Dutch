'''
Seq_SBN::: [['BOS1'], ['dog.n.01', 'Instrument', '+2'], ['golden.a.01', 'AttributeOf', '+1'], ['coat.n.03'], ['be.v.01', 'Theme', '-3', 'Time', '+1', 'Location', '+2'], ['time.n.08', 'EQU', 'now'], ['water.n.02']]
Concept::: ['BOS1', 'dog.n.01', 'golden.a.01', 'coat.n.03', 'be.v.01', 'time.n.08', 'water.n.02']
'''

import sys
from sbn_utils import read_sbn_file, apply_bpe_edge, create_structural_path

if __name__ == '__main__':
    train_file, concept_out, path_out = sys.argv[1], sys.argv[2], sys.argv[3]
    ### get all the information (nodes and edges) in the training data
    all_instances, max_node_num, max_in_neigh_num, max_out_neigh_num = read_sbn_file(train_file)

    file_lst, content_lst = [], []
    for i in range(1, 9):  # Eight paths
        f = open(path_out + '_{}'.format(i), 'w')
        content_lst.append([])
        file_lst.append(f)
    path_out = open(path_out, "w")
    all_paths, all_nodes = [], []

    with open(concept_out,'w') as concept_file:
        for index, sbn_data in enumerate(all_instances):
            nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices, out_neigh_edges = sbn_data
            concept_file.write(' '.join(nodes) + '\n')
            #print('======================{}========================='.format(index))
            #print(nodes)
            #print(in_neigh_indices)
            #print(in_neigh_edges)
            #print(out_neigh_indices)
            #print(out_neigh_edges)
            bpe_nodes = nodes
            G1, tag1, G2, tag2 = apply_bpe_edge(bpe_nodes, nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices,
                                                out_neigh_edges)
            bpe_path = create_structural_path(G1, G2, tag2)
            bpe_nodes.append('EOS')

            lineth_path = []
            kth_path = [[] for _ in range(8)]
            for i in range(len(bpe_nodes)):
                for j in range(len(bpe_nodes)):
                    lineth_path.append(''.join(bpe_path[(i, j)]))
                    for k in range(8):
                        label = bpe_path[(i, j)][k] if k < len(bpe_path[(i, j)]) else '<blank>'
                        kth_path[k].append(label)
            all_paths.append(' '.join(lineth_path) + ' ')
            for m in range(8):
                content_lst[m].append(' '.join(kth_path[m]) + ' ')

    path_out.write('\n'.join(all_paths))
    for idx, ff in enumerate(file_lst):
        ff.write('\n'.join(content_lst[idx]))






