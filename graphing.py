from master_file_cayley import Letter
from master_file_cayley import Word
from master_file_cayley import NewGroup
import os
import psutil
import networkx as nx
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
# import pickle
import time


process = psutil.Process(os.getpid())
start_time = time.time()

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")

identity = Word([])

a_word = Word([a])
b_word = Word([b])

aa = Word([a, a])
aA = Word([a, A])
bB = Word([b, B])
bb = Word([b, b])
ab = Word([a, b])
abAB = Word([a, b, A, B])
aaaa = Word([a, a, a, a])
bbbbbb = Word([b, b, b, b, b, b])
bbb = Word([b, b, b])
ababab = Word([a, b, a, b, a, b])
abab = Word([a, b, a, b])
aB = Word([a, B])
aBa = Word([a, B, a])
baB = Word([b, a, B])
Bab = Word([B, a, b])
aba = Word([a, b, a])
Ba = Word([B, a])
B_word = Word([B])
ba = Word([b, a])

G = NewGroup([a, b], [aa, bbb, aA, bB, ababab], 10)
H = nx.DiGraph()

elements = [identity]

non_e_elements = G.yield_elems_of_quotient(4, 10)
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
            if G.test_equals(elem_with_letter, member_2, 10):
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

numbers = open("products/g4_4_10.txt", 'w')

numbers.write(str(H.number_of_nodes()) + " is the number of nodes\n")
numbers.write(str(H.number_of_edges()) + " is the number of edges\n")
numbers.write(str("Run time = " + str(time.time() - start_time)))

numbers.close()

# for node in nodes:
#     print(node)
# for (u, v) in edges:
#     print(u.return_word_str(), v.return_word_str())
imagename = "products/g4_4_10.png"

plt.savefig(imagename)
