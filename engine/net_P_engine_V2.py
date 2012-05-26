#coding:utf-8
#a very simple 2-D physical engine
import numpy as np
import scipy as sci
import random
import math
import networkx as nx
import matplotlib.pyplot as plt

class Force_Field():
    def __init__(self):
        self.k_node = 50.0 
        self.k_link = 100.0 
        self.k_center = -10
        self.k_damp = -3.0
        self.ln = 0.5
        self.lk = 0.5
    def f_demp(self,v):
        return self.k_damp*v

    def f_by_nodes(self,l,m1,m2):
        return m1*m2*self.k_node/(l*l)

    def f_by_connect(self,l):
        return self.k_link*(l-self.lk)

    def f_by_o(self,l):
        return self.k_center*(l**2)

def physics_engine(G,R = None,force_field = None,total_time = None,dynamic =
        None,pngname = None,label=None):
    if len(G) <= 1:
        print "G  have more than 1 nodes"
        return None

    def coords_2_one(a):
        b = np.zeros(2,dtype=float)
        b[0] = a[0] / math.sqrt(a[0]**2 + a[1]**2)
        b[1] = a[1] / math.sqrt(a[0]**2 + a[1]**2)
        return b

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

    def draw_G(G,R,pngname,label):
        nx.draw(G,R,node_size=5,with_labels=label)
        plt.savefig(pngname,dpi=50)
        plt.clf()
    ####default_values####
    if R == None:
        R = {}
        for node in G:
            x = random.random()
            y = random.random()
            R[node] = (x,y)
    if dynamic == None:
        dynamic = True
    if pngname == None:
        pngname = "/Users/bingwang/VimWork/BioNetWork/engine/test.png"
    if total_time == None:
        total_time = 20
    if force_field == None:
        force_field = Force_Field()
    if label == None:
        label = False
    stop_E = 0.1 #constriction condition
                 #E = sum(v**2)
    dt = 0.02
    n2i = {}
    i2n = {}
    for i,node in enumerate(G):
        n2i[node] = i
        i2n[i] = node

    r = R2r(R,n2i)
    m = np.zeros((len(G),1),dtype = int)
    for node in G:
        m[n2i[node]] = G.node[node]['size']
    v = np.zeros((len(G),2),dtype = float)
    a = np.zeros((len(G),2),dtype = float)
    F_c = np.zeros((len(G),len(G)),dtype=float)
    F_n = np.zeros((len(G),len(G)),dtype=float)
    dist = np.zeros((len(G),len(G)),dtype=float)
    G_array = G2array(G,n2i)
    
    for t in range(int(total_time/dt)):
        F = np.zeros((len(G),2),dtype = float)
        #F_o = np.zeros((len(G),2),dtype = float)
        for i,item in enumerate(G):
            #F_o[i] = -coords_2_one(r[i])*math.sqrt(sum(r[i]**2))
            for j in range(len(G)):
                if j != i:
                    dist[i,j] = math.sqrt(sum((r[i]-r[j])**2))
                    if G_array[i,j]:
                        F_c[i,j] = force_field.f_by_connect(dist[i,j])
                    else:
                        F_n[i,j] = force_field.f_by_nodes(dist[i,j],m[i][0],m[j][0])

                    F[i] += coords_2_one(r[j]-r[i])*(F_n[i][j]+F_c[i][j])
        
        ##Main functions## 
        Fd = force_field.f_demp(v)
        a = (F+Fd)/m  
        dv = a * dt
        v += dv
        dr = v * dt
        r += dr
        if dynamic:
            draw_G(G,r2R(r,i2n),pngname,label)
        #######Stop condition######
        if sum(v[0]**2+v[1]**2) < stop_E:
            draw_G(G,r2R(r,i2n),pngname,label)
            return r2R(r,i2n)
    print "Hey, time too short, or cannot be astringe"
    return r2R(r,i2n)

###########main###########
if __name__ == "__main__":
    nodes = [1,2,3,4,5,6,7,8,9,10,11]
    edges = {}
    edges[1] = [2,3,4,11]
    edges[2] = [1,3,4]
    edges[3] = [4,2,1]
    edges[4] = [1,2,3]
    edges[5] = [6,7,1]
    edges[6] = [5,7]
    edges[7] = [5,6]
    edges[8] = [9,10,11]
    edges[9] = [8,10,11]
    edges[10] = [8,9]
    edges[11] = [8,9,1]
    G = nx.Graph()
    pos = {}
    for i,node in enumerate(nodes):
        G.add_node(node)
        pos[node] = (random.random(),random.random())
        for link_node in edges[node]:
            if link_node in G and link_node in G:
                G.add_edge(node,link_node)

    pos = physics_engine(G,pos,label=False)
    
    #G.add_nodes_from(nodes)
    #G.add_edges_from(edges)
    #physics_engine(G)


