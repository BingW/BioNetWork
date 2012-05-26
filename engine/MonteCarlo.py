#coding:utf-8
#A very simple MonteCarlo model
import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def cross(line1,line2):

    x1 = (line1[0][0],line1[1][0])
    y1 = (line1[0][1],line1[1][1])
    x2 = (line2[0][0],line2[1][0])
    y2 = (line2[0][1],line2[1][1])
    
    if x1[0] == x1[1]:
        if x2[0] == x2[1]:
            if x1[0] == x2[0] and (min(y2)<y1[0]<max(y2) or min(y2)<y1[1]<max(y2)):
                print "And Never"
                return True
            else:
                return False
        else:
            a2 = (y2[0]-y2[1])/(x2[0]/x2[1])
            b2 = y2[0] - a2 * x2[0]
            if min(y1) < (a2 * x1[0] + b2) < max(y1) and \
               min(y2) < (a2 * x1[0] + b2) < max(y2):
                return True
            else:
                return False
    else:
        a1 = (y1[0]-y1[1])/(x1[0]-x1[1])
        b1 = y1[0] - a1 * x1[0]
        if x2[0] == x2[1]:
            if min(y1) < (a1 * x2[0] + b1) < max(y1) and \
               min(y2) < (a1 * x2[0] + b1) < max(y2):
                return True
            else:
                return False
        else:
            a2 = (y2[0]-y2[1])/(x2[0]-x2[1])
            b2 = y2[0] - a2 * x2[0]
            if a1 == a2:
                if b1 == b2 and (min(y2)<y1[0]<max(y2) or min(y2)<y1[1]<max(y2)):
                    print "And Never"
                    return True 
                else:
                    return False
            else:
                x_0 = (b2-b1)/(a1-a2)
                if min(x1)<x_0<max(x1) and min(x2)<x_0<max(x2):
                    return True
                else:
                    return False

def cross_score(H,r):
    cross_array = np.zeros(len(r),dtype=int)
    edges = []
    edges_index = []
    for i in range(len(r)):
        for j in range(i+1,len(r),1):
            if H[i][j] == True:
                edges.append((r[i],r[j]))
                edges_index.append((i,j))

    for i in range(len(edges)):
        for j in range(0,i,1):
            if edges_index[i][0] != edges_index[j][0] and \
                edges_index[i][0] != edges_index[j][1] and\
                edges_index[i][1] != edges_index[j][0] and\
                edges_index[i][1] != edges_index[j][1]:
                if cross(edges[i],edges[j]):
                    cross_array[edges_index[i][0]] += 1
                    cross_array[edges_index[i][1]] += 1
                    cross_array[edges_index[j][0]] += 1
                    cross_array[edges_index[j][1]] += 1

    return cross_array
    
def monte_carlo(G):
    def G2array(G,n2i):
        G_array = np.zeros((len(G),len(G)),dtype=np.bool)
        for n1,n2 in G.edges():
            G_array[n2i[n1],n2i[n2]] = True
            G_array[n2i[n2],n2i[n1]] = True
        return G_array

    def R2r(R,n2i):
        r = np.zeros((len(n2i),2),dtype = float)
        for n in n2i:
            r[n2i[n]] = R[n] 
        return r
    
    def r2R(r,i2n):
        _R = {}
        for i,line in enumerate(r):
            _R[i2n[i]] = line
        return _R

    def draw_G(G,r,ID=None):
        if ID == None:
            ID = ""
        pos = {}
        for i,item in enumerate(G):
            pos[item] = (r[i][0],r[i][1])

        nx.draw(G,pos)
        plt.savefig("/Users/bingwang/VimWork/BioNetWork/engine/test.png",dpi=50)
        plt.clf()

    n2i = {}
    i2n = {}
    for i,node in enumerate(G):
        n2i[node] = i
        i2n[i] = node

    G_array = G2array(G)
    step = 10000
    r_0 = np.random.rand(len(G),2)
    r_opt = r_0
    cross_score_array = cross_score(G_array,r_0)
    best_score = sum(cross_score_array)/4

    for i in range(step):
        #v_0 = np.random.rand(len(G),2)*2-1
        #r_0 = r_opt + v_0 * 0.1
        r_0 = np.random.rand(len(G),2)
        this_cross_score_array = cross_score(G_array,r_0)
        this_score = sum(this_cross_score_array)/4

        if this_score < best_score:
            best_score = this_score
            r_opt = r_0
            draw_G(G,r_opt)
        else:
            continue
    return r_opt



###############

nodes = [1,2,3,4,5,6,7,8,9,10,11]
edges = [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),(5,6),(5,7),(6,7),(1,5),\
            (8,9),(8,10),(8,11),(9,10),(9,11),(11,1)]
#nodes = [1,2,3,4]
#edges = [(1,2),(1,3),(1,4),(2,3),(3,4)]
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
monte_carlo(G)
