from master_file_cayley import Letter, Word, NewGroup, Cayley

import os
import psutil
import networkx as nx
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time

process = psutil.Process(os.getpid())
start_time = time.time()

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")
c = Letter("c")
C = Letter("C")

identity = Word([])
aa = Word([a, a])
aA = Word([a, A])
bB = Word([b, B])
cC = Word([c, C])

ababab = Word([a, b, a, b, a, b])
bbb = Word([b, b, b])

bb = Word([b, b])
cc = Word([c, c])
abAB = Word([a, b, A, B])
bcBC = Word([b, c, B, C])
caCA = Word([c, a, C, A])

G = NewGroup([a, b, c], [aa, bb, cc, aA, bB, cC, abAB, bcBC, caCA], 10)
H = nx.DiGraph()

elements = [identity]

non_e_elements = G.yield_elems_of_quotient(4, 14)
for entry in non_e_elements:
    elements.append(entry)

color_list = ['b', 'r', 'c', 'm', 'y', 'k']

i = 0

generators = G.list_non_inv_generators()

for member in elements:
    for j in range(len(generators)):
        gen_letter = generators[j]
        elem_with_letter = Word([])
        elem_with_letter.add_word(member)
        elem_with_letter.add_letter(gen_letter)
        for member_2 in elements:
            if G.test_equals(elem_with_letter, member_2, 14):
                H.add_edges_from([(member, member_2)], color=color_list[j])
                break

    i = i + 1

nodes = H.nodes()
word_labels = {}
for i in nodes:
    word_labels[i] = i.return_word_str()

edges = H.edges()
colors = [H[u][v]['color'] for u, v in edges]

options = {
    'node_color': 'yellow',
    'node_size': 400,
}
pos = nx.spring_layout(H)

nx.draw(H, pos, **options, labels=word_labels, edge_color=colors)

numbers = open("three_gens_info.txt", 'w')

numbers.write(str(H.number_of_nodes()) + " is the number of nodes\n")
numbers.write(str(H.number_of_edges()) + " is the number of edges\n")
numbers.write(str("Run time = " + str(time.time() - start_time)))

numbers.close()

# for node in nodes:
#     print(node)
# for (u, v) in edges:
#     print(u.return_word_str(), v.return_word_str())
imagename = "three_gens_graph.png"

plt.savefig(imagename)
