import graphs as g
import bridges as b
import copy

def core(graph):
    gr = copy.deepcopy(graph)
    i = 0
    while True:
        x = list(gr.vts())[i]
        if gr.degree(x) < 2:
            gr.rmVert(x)
            i = 0
        elif gr.degree(x) == 2:
            y = list(gr.adj[x])[0]
            z = list(gr.adj[x])[1]
            gr.rmVert(x)
            gr.adj[y].add(z)
            gr.adj[z].add(y)
            i = 0
        else: 
            i = i + 1
        if i == len(gr.vts()):
            break
    return gr


def findCycle(graph):
    # use only if it is certain that minimum degree is 3
    cycle = [min(graph.vts())]
    while True:
        x = cycle[-1]
        ys = copy.deepcopy(graph.adj[x])
        if len(cycle) < 4:
            y = min([y for y in ys if y not in cycle])
            cycle.append(y)
        else: 
            ys.remove(cycle[-2])
            if len([y for y in ys if y in cycle]) < 2: 
                y = min([y for y in ys if y not in cycle])
                cycle.append(y)
            else: 
                y = [y for y in ys if y in cycle][0]
                z = [y for y in ys if y in cycle][1]
                while cycle[0] not in {y,z}:
                    cycle.pop(0)
                if cycle[0] == y:
                    chord = g.edge(x,z)
                else: 
                    chord = g.edge(x,y)
                return (cycle, chord)


def isPlanar(graph):
    gStar = core(graph)
    if len(gStar.vts()) == 0:
        return True 
    else: 
        (cycle, chord) = findCycle(gStar)
        bridges = b.bridges(graph, cycle)
        interleave = b.interleave(cycle, bridges)
        if interleave.isBipartite():
            gStar.rmEdge(chord)
            return isPlanar(gStar)
        else: 
            return False
