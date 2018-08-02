from master_file_cayley import Word, NewGroup, Letter
from whiteboard import Cayley
import psutil

a = Letter("a", 1)
b = Letter("b", 1)
c = Letter("c", 1)

A = Letter("a", -1)
B = Letter("b", -1)
C = Letter("c", -1)

aA = Word([a, A])
bB = Word([b, B])
cC = Word([c, C])

aa = Word([a, a])
bb = Word([b, b])
cc = Word([c, c])

abAB = Word([a, b, A, B])
acAC = Word([a, c, A, C])
bcBC = Word([b, c, B, C])

G = NewGroup([a, b, c], [aA, bB, cC, aa, bb, cc, abAB, acAC, bcBC], 10)

newCayley = Cayley()
newCayley.read_newgraph(G)

newCayley.draw()
