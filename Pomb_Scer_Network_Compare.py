#coding: utf-8
###########Input###############
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("/Users/bingwang/VimWork/")
import lib.read.read_orthogroups_tab as orth
###########Class###############
class Interaction_SGD():
    def __init__(self,line):
        elements = line.split("\t")
        self.bait_name = elements[0]
        self.bait_standard = elements[1]
        self.hit_name = elements[2]
        self.hit_standard = elements[3]
        self.exp_type = elements[4]
        self.Gen_or_Phy = elements[5]

        self.note = elements[8]
        self.phenotype = elements[9]
        self.Manual_or_High = elements[7]
        self.src = elements[6]
        self.ref = elements[10]
        self.ciation = elements[11]

class Interaction_BioGrid():
    def __init__(self,line):
        elements = line.split("\t")
        self.bait_name = elements[0]
        self.hit_name = elements[1]

        self.bait_standard = elements[2]
        self.hit_standard = elements[3]
        self.bait_alias = elements[4]
        self.hit_alias = elements[5]

        self.exp_type = elements[6]

        self.src = elements[7]
        self.PMID = elements[8]

############Function############
def fileter_by_type(exp_type,interactions):
    #This return a subset of interactions with specifc exe_type
    collect_interaction = []
    for interaction in interactions:
        try:
            exp_type.index(interaction.exp_type)
            collect_interaction.append(interaction)
        except:
            continue
    return collect_interaction

def write_gene_func(name_lists,write_file):
    #this write functions of name_lists to write_file
    import lib.read.read_SGD_features_tab as SGD 
    SGD_feature_tab_file = "/Users/bingwang/VimWork/db/SGD_features.tab"
    feature_table = SGD.read(SGD_feature_tab_file)
    f = open(write_file,"w")
    for name in name_list:
        index = SGD.get_feature_index(name,feature_table)
        description = feature_table[index].description
        f.write(node+"\t"+str(nx.degree(DR_net)[node])+"\t"+description+"\n")
    f.close()

def sub_by_degree(min_degree,net):
    #return a subset of net by biger than min_degree
    remove_node_list = [item for item in nx.degree(net) \
            if nx.degree(net)[item] < min_degree]
    new_net = nx.Graph()
    new_net.add_nodes_from(net.nodes())
    new_net.add_edges_from(net.edges())
    for name in remove_node_list:
        new_net.remove_node(name)
    return new_net

def draw_G(G,png=None,pos=None,r=None,node_note=None):
    if pos == None and r != None:
        pos = {}
        for i,item in enumerate(G):
            pos[item] = (r[i][0],r[i][1])
    elif r == None and pos == None:
        print "r and pos should have one"
        return None

    color = []
    nodesize = []
    for i,item in enumerate(G):
        color.append(nx.degree(G)[item])
        nodesize = 10
    if png != None:
        nx.draw(G,pos,node_size=nodesize,node_color=color,edge_color='red',style \
            = 'dashed',with_labels=True)
        if node_note != None:
            plt.
        plt.savefig(png,dpi=200)
        plt.clf()
    else:
        nx.draw(G,pos,node_size=nodesize,node_color=color,edge_color='green',style \
            = 'solid',with_labels=True)

import lib.read.read_SGD_features_tab as SGD 
SGD_feature_tab_file = "/Users/bingwang/VimWork/db/SGD_features.tab"
feature_table = SGD.read(SGD_feature_tab_file)
function_dict = {}
for item in feature_table:
    function_dict[item.feature_name] = item.description

##############    Paramters    ################
min_degree = 90
#exp_type = ["Dosage Rescue"]    #directed    -A  <-rescue- +B
#exp_type = ["Synthetic Rescue"]    #directed -A  <-rescue- -B
#exp_type = ["Dosage Lethality","Dosage Growth Defect"]    #directed  -A <-defect- +B
#exp_type = ["Positive Genetic"]   #NON direction    -A or -B   <-rescue-  -AB
#exp_type = ["Negative Genetic","Synthetic Growth Defect", \
#        "Synthetic Lethality", "Synthetic Haploinsufficiency"]   #NON direction -A or -B  <-defect-  -AB
#exp_type = ["Phenotypic Enhancement"]    #dirceted    -A or +A <- -B or +B
#exp_type = ["Phenotypic Suppression"]    #directed    -A or +A |- -B or +B
#
#exp_type = ["Biochemical Activity"]    #directed  depends
exp_type = ["Reconstituted Complex","Two-hybrid","Protein-peptide", \
    "PCA","FRET","Far Western","Co-purification","Co-localization", \
    "Co-fractionation","Co-crystal Structure","Affinity Capture-Western",\
    "Affinity Capture-MS","Affinity Capture-Luminescence"]    #NON directed

Scer_tab = "/Users/bingwang/VimWork/db/interaction_data.tab"
Spom_tab = "/Users/bingwang/VimWork/BIOGRID-ORGANISM-Schizosaccharomyces_pombe-3.1.86.tab.txt"
Scer_interactions = []
Spom_interactions = []
Scer_DR_net = nx.Graph()
Spom_DR_net = nx.Graph()
##############    Main    ###################
f = open(Scer_tab)
for line in f:
    line = line.strip()
    interaction = Interaction_SGD(line)
    Scer_interactions.append(interaction)
f.close()

f = open(Spom_tab)
while(f.readline()[0:8] != "INTERACT"):
    pass
for line in f:
    interaction = Interaction_BioGrid(line)
    Spom_interactions.append(interaction)
f.close()

for item in fileter_by_type(exp_type,Scer_interactions):
    Scer_DR_net.add_node(item.bait_name)
    Scer_DR_net.add_node(item.hit_name)
    Scer_DR_net.add_edge(item.bait_name,item.hit_name)

for item in fileter_by_type(exp_type,Spom_interactions):
    Spom_DR_net.add_node(item.bait_name)
    Spom_DR_net.add_node(item.hit_name)
    Spom_DR_net.add_edge(item.bait_name,item.hit_name)

Scer_Spom_tab = "/Users/bingwang/VimWork/db/Scer-Spom-orthologs.txt"
#Spom_Scer_tab = "/Users/bingwang/VimWork/db/Spom-Scer-orthologs.txt"
Scer_Spom = orth.read(Scer_Spom_tab)
#Spom_Scer = orth.read(Spom_Scer_tab)
Scer_orth = {}
Spom_orth = {}
Scer_net_name = Scer_DR_net.nodes()
for item in Scer_net_name:
    try:
        if Scer_Spom[item] != ['NONE'] and len(Scer_Spom[item]) == 1:
            Scer_orth[item] = Scer_Spom[item][0]
            Spom_orth[Scer_Spom[item][0]] = item
        else:
            Scer_DR_net.remove_node(item)
    except:
        Scer_DR_net.remove_node(item)

Spom_net_name = Spom_DR_net.nodes()
for i,node in enumerate(Spom_net_name):
    try:
        Spom_orth[node]
        Scer_orth[Spom_orth[node]]= True
        Spom_orth[node] = True
    except:
        Spom_DR_net.remove_node(node)

Scer_net_name = Scer_DR_net.nodes()
for i,node in enumerate(Scer_net_name):
    try:
        if Scer_orth[node] == True:
            pass
        else:
            Scer_DR_net.remove_node(node)
    except:
        Scer_DR_net.remove_node(node)

#pos_Scer = nx.circular_layout(Scer_DR_net)
#pos_Scer = nx.random_layout(Scer_DR_net)
pos_Scer = nx.shell_layout(Scer_DR_net)
pos_Spom = {}
for node in pos_Scer:
    try:
        pos_Spom[Scer_Spom[node][0]]
        print "Warning @" ,Scer_Spom[node][0]
    except:
        pos_Spom[Scer_Spom[node][0]] = pos_Scer[node]

Scer_DR_net = sub_by_degree(min_degree,Scer_DR_net)
Spom_DR_net = sub_by_degree(min_degree,Spom_DR_net)
compare_png = "/Users/bingwang/VimWork/Scer_Spom/PP_compare"+str(min_degree)+".png"
draw_G(Spom_DR_net,pos=pos_Spom)
draw_G(Scer_DR_net,pos=pos_Scer,png=compare_png,node_node=function_dict)


