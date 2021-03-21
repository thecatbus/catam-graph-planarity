import graphs as g
import core as c 
import random
import sys

# plot Platonic solids
platonic = {}
for n in [4, 6, 8, 12, 20]: 
    file = open("../data/II-17-7-Platonic_" + str(n) + ".txt")
    platonic[n] = g.fromString(file.read())
    if n in [4, 8, 20]:
        platonic[n].plotWith([1,2,3],"Q1-platonic-" + str(n))
    elif n == 6:
        platonic[n].plotWith([1,2,3,4],"Q1-platonic-" + str(n))
    else:
        platonic[n].plotWith([1,2,3,4,5],"Q1-platonic-" + str(n))

# plot k2+p5
k2PlusP5 = g.fromString("1 2\n3 4\n4 5\n5 6\n6 7")
for i in [1,2]:
    for j in [3, 4, 5, 6, 7]:
        k2PlusP5.addEdge((i,j))
k2PlusP5.plotWith([1,2,3],"Q1-k2-plus-p5")

print("k2+p5 is planar:" + str(c.isPlanar(k2PlusP5)))
print("Tetrahedron is planar:" + str(c.isPlanar(platonic[4])))
print("Dodecahedron is planar:" + str(c.isPlanar(platonic[20])))

platonic[20].addEdge((1, 10))
platonic[20].addEdge((2, 10))
print("Dodecahedron+(1,10)+(2,10) is planar:" + str(c.isPlanar(platonic[20])))

# random maximal planar graphs
def randomMaximal(n): 
    allEdges = [] 
    for i in range(n): 
        for j in range(i+1, n): 
            allEdges.append((i,j)) 
    random.shuffle(allEdges)
    graph = g.Graph({})
    rejectionsAt = []
    for i in range(len(allEdges)):
        sys.stdout.write("\rAdding edge number % i" % (i+1))
        sys.stdout.flush()
        x = allEdges[i]
        graph.addEdge(x)
        if not c.isPlanar(graph):
            rejectionsAt.append(i)
            graph.rmEdge(x)
    rejectionsAt.append(0)
    return (graph, rejectionsAt[0])

for i in range(20): 
    print("\nGenerating graph number " + str(i+1) + "...")
    (graph, n) = randomMaximal(40)
    print("\nFirst violation encountered after " + str(n) + " additions.\n")

    edges = list(graph.eds())

    f = open("../output/Q9-maximal-"+str(i+1)+".csv", "a")
    for j in range(6):
        f.write(",".join([str(x)+" "+str(y) 
                          for (x,y) in edges[19*j:19*(j+1)]]))
        f.write("\n")
    f.write("\n" + str(n))
    f.close()

    (u,v) = edges[0]
    for w in range(40):
        if g.edge(u,w) in edges and g.edge(v,w) in edges:
            graph.plotWith([u,v,w],"Q9-random-40"+str(i+1))
            print("Plotted. \n")
            break
