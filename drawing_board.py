import pickle
import networkx as nx


g = nx.Graph()

for i in range(10):
    g.add_node(i+1)
    for node in g.nodes():
        if (i+1)*node == 10:
            g.add_edge(i+1, node)

print(g.nodes())
print(g.edges())

pickle.dump(g, open('pickles/testing1', 'wb'))

h = pickle.load(open('pickles/testing', 'rb'))

print(h.nodes())
print(h.edges())