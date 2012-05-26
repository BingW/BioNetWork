#coding:utf-8
#A very simple MonteCarlo model
import sys
import math
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def is_cross(line1,line2):
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

def fitness(G,R):
    cross = 0
    edges = G.edges() 
    for i in range(len(edges)):
        for j in range(0,i,1):
            if edges[i][0] != edges[j][0] and \
                edges[i][0] != edges[j][1] and \
                edges[i][1] != edges[j][0] and \
                edges[i][1] != edges[j][1]:
                if is_cross((R[edges[i][0]],R[edges[i][1]]),\
                    (R[edges[j][0]],R[edges[j][1]])):
                    cross += 1
    return cross

def fitness2(G,R):
    total_length = 0
    edges = G.edges()
    for edge in edges:
        total_length += math.sqrt(sum((R[edge[0]] - R[edge[1]])**2))
    return total_length

def cross_change(list_1,list_2):
    a = list_1[:]
    b = list_2[:]
    length = len(a)
    cross_pos = random.randint(0,length-1)
    a[cross_pos],b[cross_pos] = b[cross_pos],a[cross_pos]
    node = a[cross_pos]
    changed_index = [cross_pos]
    while a.count(node) != 1:
        for i,n in enumerate(a):
            if n == node and i not in changed_index:
                a[i],b[i] = b[i],a[i]
                changed_index.append(i)
                node = a[i]
    for node in a:
        if a.count(node) > 1:
            print "ca"
    return (a,b)

def self_change(list_1):
    q = list_1[:]
    a = random.randint(0,len(list_1)-1)
    b = random.randint(0,len(list_1)-1)
    q[a],q[b] = q[b],q[a]
    return q

def duplicate(now_reps,to_num):
    len_reps = len(now_reps)
    new_reps = now_reps[:]
    while len(new_reps) < to_num:
        a = random.randint(0,len_reps-1)
        b = random.randint(0,len_reps-1)
        new_1,new_2 = cross_change(now_reps[a],now_reps[b])
        new_reps.append(self_change(new_1))
        new_reps.append(self_change(new_2))
    return new_reps

def draw_G(G,pngname,R = None):
    if R == None:
        G = nx.relabel_nodes(G,slim_dict)
        R = nx.get_node_attributes(G,'pos')
    node_size = []
    node_color = []
    for node in G:
        size = math.log(G.node[node]["size"],2)*100
        #size = G.node[node]["size"]
        node_size.append(size)
        #node_color.append(G.node[node]["color"])
    nx.draw_networkx_nodes(G,R,node_size=node_size,node_color="white",cmap=plt.cm.autumn)
    for edge in G.edges():
        width = math.log(G[edge[0]][edge[1]]["weight"],2)
        percent = G[edge[0]][edge[1]]["percent"]
        nx.draw_networkx_edges(G,R,edgelist=[edge],width=width,alpha=percent)
    #nx.draw_networkx_labels(G,R,font_size=10)
    plt.xlim(-1.6,1.6)
    plt.ylim(-1.6,1.6)
    plt.axis('off')
    plt.savefig(pngname,dpi=200)
    plt.clf()

def genetic(G,fit):
    print len(G)
    def rep2R(rep):
        R = {}
        for i,node in enumerate(rep):
            R[node] = pos_list[i]
        return R 
    rep_num = 20
    select = 3
#--------------init-------------------
    reps = []
    pos_list = []
    node_list = []
    for i,node in enumerate(G):
        node_list.append(node)
        pos_list.append(G.node[node]["pos"])
    best_order = node_list
    best_score = fitness(G,rep2R(node_list)) if fit == "C" else fitness2(G,rep2R(node_list))
    best_score_count = 0
    count = 0
    for i in range(rep_num):
        random.shuffle(node_list)
        reps.append(node_list[:]) #hard copy
#-------------loop------------------------
    for i in range(10000):
        if best_score_count > 20:
            break
        fitness_list = []
        for rep in reps:
            R = rep2R(rep)
            score = fitness(G,R) if fit == "C" else fitness2(G,R) 
            if score < best_score:
                best_score = score
                best_score_count = 0
                best_order = rep
                if fit == "C":
                    draw_G(G,"/Users/bingwang/VimWork/BioNetWork/Genetic_Cross/"+str(count)+".png",R)
                else:
                    draw_G(G,"/Users/bingwang/VimWork/BioNetWork/Genetic_Length/"+str(count)+".png",R)
                count += 1
            fitness_list.append(score)
        print fitness_list
        cut_off = sorted(fitness_list)[select]

        reps = duplicate([reps[i] for i,score in enumerate(fitness_list) if
            score <= cut_off],rep_num)
        best_score_count += 1
#---------------end-----------------------
    return rep2R(best_order)
