from master_file_cayley import Letter
from master_file_cayley import Word
from master_file_cayley import WordTrie
from master_file_cayley import NewGroup
import time
import os
import psutil
import networkx as nx
import matplotlib.pyplot as plt

process = psutil.Process(os.getpid())


print(process.memory_info().rss / 10 ** 6)

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

denom = int(input("denominator? numbers only please "))
group = str(input("what group is this? i.e. g2, g3, etc. "))
versionnum = str(input("what version i.e. 1, 2, etc. "))

G = NewGroup([a, b], [aa, bbbbbb, aA, bB, abab], denom)

H = nx.Graph()

elements = [identity]

yielding_elts = G.yield_elems_of_quotient(4, denom)

color_list = ['b', 'r', 'c', 'm', 'y', 'k']

for entry in yielding_elts:
    elements.append(entry)
    print(entry)

i = 0

generators = G.list_non_inv_generators()

print(generators)

for member in elements:
    print(member)
    for j in range(len(generators)):
        gen_letter = generators[j]
        elem_with_letter = Word([])
        elem_with_letter.add_word(member)
        elem_with_letter.add_letter(gen_letter)
        for member_2 in elements:
            if G.test_equals_old(elem_with_letter, member_2, denom):
                print(member.return_word_str() + " is connected to " + member_2.return_word_str() +
                      " by " + gen_letter.get_str())
                H.add_edges_from([(member, member_2)], color=color_list[j])
                break

    i = i + 1
    print(str(i) + " out of " + str(len(elements)) + " completed \n")

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

print(str(H.number_of_nodes()) + " is the number of nodes")
print(str(H.number_of_edges()) + " is the number of edges")

# for node in nodes:
#     print(node)
# for (u, v) in edges:
#     print(u.return_word_str(), v.return_word_str())
imagename = "ngroup.cayley." + group + ".(4," + str(denom) + ") - " + versionnum + ".png"

plt.savefig(imagename)
plt.show()
