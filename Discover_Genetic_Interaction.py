# -*- coding:utf-8 -*-
'''
Author: Bing Wang
Last Modified: 2012.3.23
Version: V0.01
'''
WORKPATH = "/Users/bingwang/VimWork/"
#########################
#######Imput#############
import os
import sys
import time
import math
import numpy as np
import networkx as nx
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
sys.path.append("/Users/bingwang/VimWork/")
import lib.func.read as read

###########Class###############

interaction_file = "/Users/bingwang/VimWork/db/interaction_data.tab"
interactions = []
PP_net = nx.Graph()

f = open(interaction_file)
for line in f:
    line = line.strip()
    interaction = read.SGD_Interaction(line)
    interactions.append(interaction)
f.close()

PP_exp_type = ["Reconstituted Complex","Two-hybrid","Protein-peptide", \
    "PCA","FRET","Far Western","Co-purification","Co-localization", \
    "Co-fractionation","Co-crystal Structure","Affinity Capture-Western",\
    "Affinity Capture-MS","Affinity Capture-Luminescence"]    #NON directed

Ge_exp_type = ["Dosage Rescue"]    #directed    -A  <-rescue- +B
#Ge_exp_type = ["Synthetic Rescue"]    #directed -A  <-rescue- -B
#Ge_exp_type = ["Dosage Lethality","Dosage Growth Defect"]    #directed  -A <-defect- +B
#Ge_exp_type = ["Positive Genetic"]   #NON direction    -A or -B   <-rescue-  -AB
#Ge_exp_type = ["Negative Genetic","Synthetic Growth Defect", \
#           "Synthetic Lethality", "Synthetic Haploinsufficiency"]   #NON direction -A or -B  <-defect-  -AB
#Ge_exp_type = ["Phenotypic Enhancement"]    #dirceted    -A or +A <- -B or +B
#Ge_exp_type = ["Phenotypic Suppression"]    #directed    -A or +A |- -B or +B
'''

for item in interactions_filter(interactions,condition):
    PP_net.add_node(item.bait_name)
    PP_net.add_node(item.hit_name)
    PP_net.add_edge(item.bait_name,item.hit_name)

pos = nx.circular_layout(PP_net)
for item in PP_net:
    pos[item] -= 0.5
    try:
        gal_genes.index(item)
    except:
        pos[item] *= 3
p1_genes = [name for name in PP_net]

tail="/Users/bingwang/VimWork/output/functions/left_tail_of_Agos_Klac_Sklu.txt"

p0_rate = {}
f = open(tail)
for line in f:
    elements = line.split("\t")
    p0_rate[elements[4]] = elements[0]

count = 0
for item in p0_rate:
    try:
        p1_genes.index(item)
        count += 1
    except:
        continue
nodesize = [nx.degree(PP_net)[item]+min_degree for item in PP_net]
Phy.physics_engine(PP_net)

print "p value:",p_value(count,len(p0_rate),len(p1_genes)*1./3070)
nx.draw(PP_net,pos,node_size=nodesize,with_labels=True)
plt.savefig("/Users/bingwang/VimWork/PP_Gal_"+str(min_degree)+".png",dpi=300)
plt.clf()
'''
