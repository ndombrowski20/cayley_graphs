from master_file_cayley import Letter
from master_file_cayley import Word
from master_file_cayley import WordTrie
from master_file_cayley import NewGroup
from graphviz import Digraph

import time
import os
import psutil
import networkx as nx
import matplotlib.pyplot as plt
import pickle

process = psutil.Process(os.getpid())


print(process.memory_info().rss / 10 ** 6)

class Cayley:
    # the purpose of this class is to store the data from previously
    # generated Groups and produce Cayley graphs from that data. In fact,
    # if I can, I can also create a program that will output a bunch of
    # text that can be fed into different
    def __init__(self):
        self._paranoid = True
        self._graph = nx.Graph()

    def read_newgraph(self, a_group):
        # this is the same code i've been using to output all of the group graphics so far (so any and
        # all networkx/matplotlib graphics). i allowed for the user to input the numerator and denominator
        # as that would be simpler. the purpose of this class is in part to limit the computational effort
        # for each yielding of edges, etc. However, if this is just being called and the graph hasn't been
        # constructed yet then we might as well give the user some choice.
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("only groups with this method")

        num1 = int(input("numerator? "))
        num2 = int(input("denominator? "))

        color_list = ['b', 'r', 'c', 'm', 'y', 'k']

        identity = Word([])
        elements = [identity]
        non_e_elements = a_group.yield_elems_of_quotient(num1, num2)
        for entry in non_e_elements:
            elements.append(entry)

        i = 0

        generators = a_group.list_non_inv_generators()

        for member in elements:
            # print(member)
            for j in range(len(generators)):
                gen_letter = generators[j]
                elem_with_letter = Word([])
                elem_with_letter.add_word(member)
                elem_with_letter.add_letter(gen_letter)
                # print(elem_with_letter)
                for member_2 in elements:
                    if a_group.test_equals(elem_with_letter, member_2, num2):
                        # print(elem_with_letter.return_word_str() + " == " + member_2.return_word_str())
                        # print(member.return_word_str() + " is connected to " + member_2.return_word_str() +
                              # " by " + gen_letter.get_str())

                        self._graph.add_edges_from([(member, member_2)], color=color_list[j])
                        self._graph.node[member_2]['word'] = member_2.return_word_str()
                        break

            i = i + 1
            # print(str(i) + " out of " + str(len(elements)) + " completed \n")

        # print(str(self._graph.number_of_nodes()) + " is the number of nodes")
        # print(str(self._graph.number_of_edges()) + " is the number of edges")

        pickel = input("Do you want me to pickle this graph? Y/N ")
        if pickel == 'Y':
            self.pickle_me()

    def read_pickle(self, a_str):
        self._graph = pickle.load(open(a_str))

        if not self._graph.nodes():
            raise Exception("there might be a problem, no nodes")

    def feed_pickle(self):
        file_name = input("Please type the exact document name into this input."
                          "it must be exactly the same and might have to be saved "
                          "where this file is saved")

        self.read_pickle(file_name)

    def draw(self):
        # this just takes the edges and creates a dictionary of a node being the keys to the other nodes that
        # it is connected to. This way we can see what Words are connected to one another.
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("There's nothing to print, you haven't populated me with a graph yet")

        # word labels
        word_labels = {}
        for i in self._graph.nodes():
            word_labels[i] = i.return_word_str()

        # edge colors
        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u, v in edges]

        options = {
            'node_color': 'yellow',
            'node_size': 400,
        }
        pos = nx.spring_layout(self._graph)

        pickel = input("Do you want me to pickle this graph? Y/N ")
        if pickel.lower() == 'y':
            self.pickle_me()

        save_file = input("Do you want me to save this file? Y/N ")
        if save_file.lower() == 'y':
            denom = int(input("denominator? numbers only please "))
            group = str(input("what group is this? i.e. g2, g3, etc. "))
            version_num = str(input("what version i.e. 1, 2, etc. "))
            imagename = "ngroup.cayley." + group + ".(4," + str(denom) + ") - " + version_num + ".png"
            plt.savefig(imagename)

        print(str(self._graph.number_of_nodes()) + " is the number of nodes")
        print(str(self._graph.number_of_edges()) + " is the number of edges")

        plt.subplot()
        nx.draw(self._graph, pos, **options, labels=word_labels, edge_color=colors)
        plt.show()

    def pickle_me(self):
        filename = input("What do you want me to name the pickle file")

        pickle.dump(self._graph, open(filename, 'w'))

    def export_gv(self):
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("I need a graph first")

        graphviz_output = Digraph()

        nodes = self._graph.nodes()
        for node in nodes:
            graphviz_output.node(node.return_word_str())

        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u,v in edges]
        i = 0
        for (u, v) in edges:
            graphviz_output.edge(u, v, colors[i])
            i = i+1


num = int(input("Max num? "))

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
abAB = Word([a, b, A, B])

G = NewGroup([a, b], [aa, bb, aA, bB, abAB], num)

newCayley = Cayley()

newCayley.read_newgraph(G)
newCayley.draw()
