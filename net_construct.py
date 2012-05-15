#conding:utf-8
import sqlite3
import os
import math
import random
import numpy as np
import networkx as nx
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#
#Ge_exp_type = ["Dosage Rescue"]                                     #directed         -A        <-rescue-  +B
#Ge_exp_type = ["Synthetic Rescue"]                                  #directed         -A        <-rescue-  -B
#Ge_exp_type = ["Dosage Lethality","Dosage Growth Defect"]           #directed         -A        <-defect-  +B
#Ge_exp_type = ["Phenotypic Enhancement"]                            #dirceted         -A or +A  <-----  -B or +B
#Ge_exp_type = ["Phenotypic Suppression"]                            #directed         -A or +A  |-----  -B or +B
#Ge_exp_type = ["Positive Genetic"]                                  #NON direction    -A or -B  <-rescue-  -AB
#Ge_exp_type = ["Negative Genetic","Synthetic Growth Defect", \
#           "Synthetic Lethality", "Synthetic Haploinsufficiency"]   #NON direction    -A or -B  <-defect-  -AB
#
#TABLE CID2condition (CID,condition) #CID = PMID_index_cindex
#TABLE PMID2readme (PMID,README)
#TABLE other2ID (other unique, SGDID)
#TABLE microarray (SGDID,CID,EXP,EXP_bool)
#TABLE ID2Interact (SGDID_1, SGDID_2, GP, ExpType, Phenotype)
#TABLE ID2Feature (SGDID, feature, stardand, Type, Descrip)
#TABLE ID2Product (SGDID, product)
#TABLE ID2Phenotype (SGDID, mutan_type, phenotype, chemical, condition, details, reporter)
#TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)

def get_other2ID():
    _other2ID = {}
    for row in C.execute("SELECT * FROM other2ID"):
        _other2ID[row[0]] = row[1]
    return _other2ID

def get_GO_group(GOID):
    _Group = []
    for row in C.execute("SELECT SGDID FROM ID2GO WHERE GOID = (?)",(GOID,)):
        if row[0] not in _Group:
            _Group.append(row[0])
    return _Group

def get_ID2Interact():
    _ID2Interact = {}
    for row in C.execute("SELECT SGDID_1,SGDID_2,GP FROM ID2Interact"):
        if row[0] not in _ID2Interact:
            _ID2Interact[row[0]] = {}
        if row[1] not in _ID2Interact:
            _ID2Interact[row[1]] = {}
        if row[1] not in _ID2Interact[row[0]]:
            _ID2Interact[row[0]][row[1]] = row[2]
        if row[0] not in _ID2Interact[row[1]]:
            _ID2Interact[row[1]][row[0]] = row[2]
    return _ID2Interact

    

def net_stage_1(group):
    _PG_interact = {}
    for row in C.execute("SELECT SGDID_1,SGDID_2 FROM ID2Interact"):
        if row[0] not in group or row[1] not in group:
            continue
        if row[0] not in _PG_interact:
            _PG_interact[row[0]] = {}
        if row[1] not in _PG_interact:
            _PG_interact[row[1]] = {}
        if row[1] not in _PG_interact[row[0]]:
            _PG_interact[row[0]][row[1]] = "U"
        if row[0] not in _PG_interact[row[1]]:
            _PG_interact[row[1]][row[0]] = "U"
    return _PG_interact

def module_seperate(ID2net):
    # L1 ID2net should be dict[ID] = {ID1:"",ID2:"",ID3:""...}
    _mod_groups = {}
    _node_viewed = []
    _stop_degree = 2
    while len(_node_viewed) < len(ID2net):
        _max_degree = 0
        _max_id = None
        for _ID in ID2net:
            if _ID in _node_viewed:
                continue
            _degree = len([n for n in ID2net[_ID] if n not in _node_viewed])
            if _degree > _max_degree:
                _max_degree = _degree
                _max_id = _ID

        if _max_degree < _stop_degree:
            break

        _mod_groups[_max_id] = [_max_id]
        _node_viewed.append(_max_id)

        _node_remove = []
        for _ID in ID2net[_max_id]:
            if _ID in _node_viewed:
                continue
            _degree = len([n for n in ID2net[_ID] if n in ID2net[_max_id] and n != _max_id])
            if _degree == 0:
                _node_remove.append(_ID)

        for _ID in ID2net[_max_id]:
            if _ID not in _node_viewed and _ID not in _node_remove:
                _node_viewed.append(_ID)
                _mod_groups[_max_id].append(_ID)
    return _mod_groups

def get_microarray(group):
    #TABLE microarray (SGDID,CID,EXP,EXP_bool)
    _SQL = "SELECT * FROM microarray WHERE "
    for ID in group[:-1]:
        _SQL += "SGDID = \'"+ID+"\' OR "
    _SQL += "SGDID = \'"+ID+"\'"
    _ID2EXP = {}
    for row in C.execute(_SQL):
        if row[0] not in _ID2EXP:
            _ID2EXP[row[0]] = {}
        _ID2EXP[row[0]][row[1]] = (row[3],row[2])
        #_ID2EXP[SGDID][CID] = (EXP_bool,EXP)
    return _ID2EXP

def draw_G(G,R,pngname,label):
        nx.draw(G,R,node_size=5,with_labels=label)
        plt.savefig(pngname,dpi=50)
        plt.clf()

def calculate_function(gene):
    def M_one_node(node_0,node_1):
        M_array = np.zeros((8133,2),dtype = np.int8)
        line_0 = SGDID_list.index(node_0)
        line_1 = SGDID_list.index(node_1)
        M_array[:,0] = Microarray[:,line_0] 
        M_array[:,1] = Microarray[:,line_1] 
        return M_array

    def M_two_nodes(node_0,node_1,node_2):
        M_array = np.zeros((8133,3),dtype = np.int8)
        line_0 = SGDID_list.index(node_0)
        line_1 = SGDID_list.index(node_1)
        line_2 = SGDID_list.index(node_2)
        M_array[:,0] = Microarray[:,line_0] 
        M_array[:,1] = Microarray[:,line_1] 
        M_array[:,2] = Microarray[:,line_2] 
        return M_array

    def bayes_one_nodes(M_array):
        count_array = np.zeros((3,3),dtype = int)
        for line in M_array:
            if 99 in line:
                continue
            else:
                node_0 = 2 if line[0] == -1 else line[0]
                node_1 = 2 if line[1] == -1 else line[1]
                count_array[node_0,node_1] += 1
        return count_array

    def bayes_two_nodes(M_array):
        count_array = np.zeros((3,3,3),dtype = int)
        for line in M_array:
            if 99 in line:
                continue
            else:
                node_0 = 2 if line[0] == -1 else line[0]
                node_1 = 2 if line[1] == -1 else line[1]
                node_2 = 2 if line[2] == -1 else line[2]
                count_array[node_0,node_1,node_2] += 1
        return count_array

    node_0 = gene.SGDID
    input_nodes = gene.input_nodes
    similar_percent = 0.95
    minimal_sum = 20 #P_value < 10^-7
    for i,node_1 in enumerate(input_nodes):
        count_array_1 = bayes_one_nodes(M_one_node(node_0,node_1))
        cord_1 = count_array_1.argmax(axis=0)
        sum_1 = count_array_1.sum(axis=0)
        percent_1 = count_array_1.max(axis=0)*1.0/sum_1
        for i_m,m in enumerate(cord_1):
            if sum_1[i_m] > minimal_sum and percent_1[i_m] > similar_percent:
                print i_m,node_1,"=>",m,node_0,"confi:",percent_1[i_m]
        for node_2 in input_nodes[i+1:]:
            count_array_2 = bayes_two_nodes(M_two_nodes(node_0,node_1,node_2))
            cord_2 = count_array_2.argmax(axis=0)
            sum_2 = count_array_2.sum(axis=0)
            percent_2 = count_array_2.max(axis=0)*1.0/sum_2
            for i_m,m in enumerate(cord_2):
                for j_n,n in enumerate(m):
                    if sum_2[i_m,j_n] > minimal_sum and percent_2[i_m,j_n] > similar_percent:
                        print i_m,node_1,"AND",j_n,node_2,"=>",n,node_0,"confi:",percent_2[i_m,j_n]

class gene_node():
    def __init__(self,ID):
        self.SGDID = ID
        self.input_nodes = [node for node in ID2input_dict[ID] if node != ID]
        self.status = 0

'''
Coon = sqlite3.connect("/Users/bingwang/VimWork/db/Scer.db")
C = Coon.cursor()
other2ID = get_other2ID()
ID2input_dict = get_ID2Interact()
print "ID2input_dict init finish!"

#ID2net[Node_1][Node_2] 
# Stage 1:    "U"               -  Linked but unknown
# Stage 2:    "12NP3"           -  12 negative correlation 3 positive correlation
# Stage 3:    "A","bA","S","bS" -  Activate, be Activated, Suppress, be Suppressed

#INIT_group = get_GO_group("GO:0006281") #DNA repair
#ID2NetL1 = net_stage_1(INIT_group)

f = open("/Users/bingwang/VimWork/db/ScerMicro_b.tab")
SGDID_list = f.readline().split("\t")[1:-1] #because nothing after the last '\t'
Microarray = np.zeros((8133,len(SGDID_list)),dtype = np.int8)
for i,line in enumerate(f):
    elements = line.split("\t")[:-1] #because nothing after the last '\t'
    for j,num in enumerate(elements[1:]):
        try:
            Microarray[i,j] = num
        except:
            Microarray[i,j] = 99
    if i%20 == 0:
        print "loding Microarray "+str(round(i*100.0/8134,2))+"%"

print "Microarray init finish!"
'''

for node in SGDID_list:
    if node in ID2input_dict:
        gene = gene_node(node)
        calculate_function(gene)
    else:
        print "node lack data "+node

#a = np.array([[[5085,109,94],[215,24,34],[487,35,83]],[[222,60,15],[45,109,9],[199,11,42]],[[242,10,33],[52,4,26],[43,9,90]]])
#a = np.array([[5917,84,207],[508,117,81],[321,11,191]])
