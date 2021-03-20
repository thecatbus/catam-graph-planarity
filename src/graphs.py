import math
import numpy as np
import matplotlib.pyplot as plt

def edge(x,y):
    if x < y:
        return (x,y)
    else:
        return (y,x)


class Graph:
    def __init__(self, adj):
        self.adj = adj # dict{vtx : ngb set}

    def vts(self): # list[vtx]
        return self.adj.keys() 

    def eds(self): # list[(v1,v2)]
        eds = set()
        for x in self.vts():
            for y in self.adj[x]: 
                eds.add(edge(x,y))
        return eds

    def degree(self, x):
        return len(self.adj[x])

    def addEdge(self, e):
        for x in e: 
            if x not in self.vts():
                self.adj[x] = set()
        self.adj[e[0]].add(e[1])
        self.adj[e[1]].add(e[0])
        return ()

    def rmEdge(self, e): 
        (x,y) = e
        if edge(x,y) not in self.eds():
            print(e)
            print(self.adj)
        self.adj[x].remove(y)
        self.adj[y].remove(x)
        return ()

    def rmVert(self,x):
        self.adj.pop(x)
        for y in self.vts():
            self.adj[y].discard(x)
        return ()

    def plotWith(self, cycle, name):
        xCoord = {}
        yCoord = {}
        body = [x for x in self.vts() if x not in cycle]
        # coordinates of cycle
        for i in range(len(cycle)):
            xCoord[cycle[i]] = math.sin(2 * math.pi * i / len(cycle))
            yCoord[cycle[i]] = math.cos(2 * math.pi * i / len(cycle))
        # matrix of coefficients
        mat = []
        for x in body:
            coeffs = []
            for y in body:
                if y == x:
                    coeffs.append(len(self.adj[x]))
                elif y in self.adj[x]: 
                    coeffs.append(-1)
                else:
                    coeffs.append(0)
            mat.append(coeffs)
        mat = np.matrix(mat)
        # constant terms
        xConst = np.matrix([ sum([xCoord[y] 
                                  for y in cycle 
                                  if y in self.adj[x]]) 
                             for x in body ])
        yConst = np.matrix([ sum([yCoord[y] 
                                  for y in cycle 
                                  if y in self.adj[x]])
                             for x in body ])
        # coordinate computation 
        xVals = np.matmul(mat.I, xConst.T)
        yVals = np.matmul(mat.I, yConst.T)
        for i in range(len(body)):
            xCoord[body[i]] = xVals.item(i,0)
            yCoord[body[i]] = yVals.item(i,0)
        # plot
        plt.clf()
        for e in self.eds():
            xs = np.array([xCoord[v] for v in e])
            ys = np.array([yCoord[v] for v in e])
            plt.plot(xs, ys, c='black', lw='0.5')
        xs = np.array([xCoord[v] for v in self.vts()])
        ys = np.array([yCoord[v] for v in self.vts()])
        plt.plot(xs, ys, marker='o', ms=0.7, c='black', ls='')
        plt.axis('off')
        plt.savefig('../output/' + name + '.pdf', 
                    bbox_inches='tight')
        return ()

    def components(self): # list[set{vts}]
        vertSet = set(self.vts())
        components = []
        def expand(c):
            d = c.copy()
            for x in c:
                d.update(self.adj[x])
            return d
        while vertSet: 
            x = min(vertSet)
            xcomp = {x}
            while len(expand(xcomp)) != len(xcomp):
                xcomp = expand(xcomp)
            vertSet.difference_update(xcomp)
            components.append(xcomp)
        return components

    def isBipartite(self):
        def connectedBipartite(comp):
            red = {min(comp)}
            blue = set()
            def expandColouring():
                for r in red:
                    blue.update(self.adj[r])
                for b in blue:
                    red.update(self.adj[b])
                if red.intersection(blue):
                    return False 
                else: 
                    return True
            xs = comp.copy()
            while xs:
                if expandColouring(): 
                    xs.difference_update(red)
                    xs.difference_update(blue)
                else: 
                    return False
            return expandColouring()
        for c in self.components():
            if not connectedBipartite(c):
                return False 
        return True


def fromString(edges):
    xs = edges.splitlines()
    adj = {}
    for x in xs:
        x = x.strip().replace('  ',' ')
        ys = list(map(int, x.split(" ")))
        for y in ys:
            if y not in adj:
                adj[y]=set()
        adj[ys[0]].add(ys[1])
        adj[ys[1]].add(ys[0])
    return Graph(adj)
