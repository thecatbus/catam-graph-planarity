import graphs as g
import copy 

def bridges(graph, cycle):
    bridges = []
    # find chords
    for i in range(len(cycle)):
        x = cycle[i]
        x1 = cycle[ (i - 1) % len(cycle)]
        x2 = cycle[ (i + 1) % len(cycle)]
        for y in graph.adj[x]:
            if y in cycle and y not in {x1, x2} and y < x:
                bridges.append({x,y})
    # find bridges
    tempGraph = copy.deepcopy(graph)
    for x in cycle:
        tempGraph.rmVert(x)
    for c in tempGraph.components():
        d = c.copy()
        for x in c:
            for y in cycle:
                if y in graph.adj[x]: 
                    d.add(y)
        bridges.append(d)
    return bridges

def interleave(cycle, bridges): 
    # vertices of attachment in cycle order
    def attachVerts(br):
        return [x for x in cycle if x in br]
    # check if bridges interleave
    def isInterleaf(b1, b2):
        xs = attachVerts(b1)
        ys = attachVerts(b2)
        if len(xs) == 3 and xs == ys:
            return True
        else:
            changes = 0
            cur = ""
            for i in cycle:
                if cur == "":
                    if i in xs:
                        cur += 'x'
                    if i in ys:
                        cur += 'y'
                elif cur == "x":
                    if i in ys: 
                        changes += 1
                        cur = "" 
                        if i in xs:
                            cur += 'x'
                        cur += 'y'
                elif cur == "y": 
                    if i in xs: 
                        changes += 1
                        cur = "" 
                        cur += 'x'
                        if i in ys:
                            cur += 'y'
                else: 
                    if (i in xs) or (i in ys):
                        changes += 1
                        cur = "" 
                        if i in xs: 
                            cur += 'x'
                        if i in ys:
                            cur += 'y'
            return (changes >= 3)

    # create graph
    adj = {}
    for i in range(len(bridges)):
        adj[i] = set()
        for j in range(len(bridges)):
            if j != i and isInterleaf(bridges[i], bridges[j]):
                adj[i].add(j)
    return g.Graph(adj)
