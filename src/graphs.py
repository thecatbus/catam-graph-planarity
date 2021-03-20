import math
import numpy as np
import matplotlib.pyplot as plt

def toAdj(edges):
    xs = edges.splitlines()
    adj = {}
    for x in xs:
        ys = list(map(int, x.split(" ")))
        for y in ys:
            if y not in adj:
                adj[y]=set()
        adj[ys[0]].add(ys[1])
        adj[ys[1]].add(ys[0])
    return(adj)

class Graph:
    def __init__(self, edgestring, name):
        self.name = name # string
        self.adj = toAdj(edgestring) # dict{vtx : ngb set}

    def vts(self):
        return self.adj.keys() # list[vtx]

    def eds(self):
        eds = set()
        for x in self.vts():
            for y in self.adj[x]: 
                if x<y: 
                    eds.add((x,y))
                else: 
                    eds.add((y,x))
        return eds

    def plotWith(self, cycle):
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
        for e in self.eds():
            xs = np.array([xCoord[v] for v in e])
            ys = np.array([yCoord[v] for v in e])
            plt.plot(xs, ys, c='black', lw='0.5')
        xs = np.array([xCoord[v] for v in self.vts()])
        ys = np.array([yCoord[v] for v in self.vts()])
        plt.plot(xs, ys, marker='o', c='black', ls='')
        plt.axis('off')
        plt.savefig('../output/' + self.name + '.png', 
                    transparent=True,
                    bbox_inches='tight')
