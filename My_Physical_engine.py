#coding:utf-8
#a very simple 2-D physical engine
import numpy as np
import scipy as sci
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
    def f_by_nodes(self,l):
        if l > self.ln:
            return 0
        else:
            return self.k_node*(l-self.ln)
    def f_by_connect(self,l):
        return self.k_link*(l-self.lk)
    def f_by_o(self,l):
        return self.k_center*(l**2)

def coords_2_one(a):
    b = np.zeros(2,dtype=float)
    b[0] = a[0] / math.sqrt(a[0]**2 + a[1]**2)
    b[1] = a[1] / math.sqrt(a[0]**2 + a[1]**2)
    return b

def G_2_array(G):
    for i,n in enumerate(G):
        G.node[n]['index'] = i

    G_array = np.zeros((len(G),len(G)),dtype=np.bool)
    for i,p1 in enumerate(G):
        for p2 in G[p1]:
            j = G.node[p2]['index']
            G_array[i,j] = True
    return G_array

def physics_engine(G,force_field = None,dt = None,total_time = None):
    if dt == None:
        dt = 0.02
    if total_time == None:
        total_time = 20
    if force_field == None:
        force_field = Force_Field()

    ####default_values####
    stop_E = 0.1 #constriction condition
                 #E = sum(v**2)

    r = np.random.rand(len(G),2)
    v = np.zeros((len(G),2),dtype = float)
    a = np.zeros((len(G),2),dtype = float)
    m = np.ones((len(G),2),dtype = float)
    F_c = np.zeros((len(G),len(G)),dtype=float)
    F_n = np.zeros((len(G),len(G)),dtype=float)
    dist = np.zeros((len(G),len(G)),dtype=float)
    G_array = G_2_array(G)
    
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
                        F_n[i,j] = force_field.f_by_nodes(dist[i,j])

                    F[i] += coords_2_one(r[j]-r[i])*(F_n[i][j]+F_c[i][j])
        
        ##Main functions## 
        Fd = force_field.f_demp(v)
        a = (F+Fd)/m  
        dv = a * dt
        v += dv
        dr = v * dt
        r += dr
        draw_G(G,r)
        #######Stop condition######
        if sum(v[0]**2+v[1]**2) < stop_E:
            return r
    print "Hey, time too short, or cannot be astringe"
    return r

def draw_G(G,r,ID=None):
    if ID == None:
        ID = ""
    color = []
    pos = {}
    for i,item in enumerate(G):
        color.append(i)
        pos[item] = (r[i][0],r[i][1])
    nx.draw(G,pos,node_size=5,node_color=color,with_labels=False)
    plt.savefig("/Users/bingwang/VimWork/Physics/test"+ID+".png",dpi=50)
    plt.clf()

###########main###########
if __name__ == "__main__":
    nodes = [1,2,3,4,5,6,7,8,9,10,11]
    edges = [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),(5,6),(5,7),(6,7),(1,5),\
            (8,9),(8,10),(8,11),(9,10),(9,11),(11,1)]
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    physics_engine(G)


