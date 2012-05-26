#conding:utf-8
import sqlite3
import numpy as np
import time
import random
import math
import json
import networkx as nx
import matplotlib.pyplot as plt

#TABLE CID2condition (CID,condition) #CID = PMID_index_cindex
#TABLE PMID2readme (PMID,README)
#TABLE other2ID (other unique, SGDID)
#TABLE microarray (SGDID,CID,EXP,EXP_bool)
#TABLE ID2Interact (SGDID_1, SGDID_2, GP, ExpType, Phenotype)
#TABLE ID2Feature (SGDID, feature, stardand, Type, Descrip)
#TABLE ID2Product (SGDID, product)
#TABLE ID2Phenotype (SGDID, mutan_type, phenotype, chemical, condition, details, reporter)
#TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)
class gene_node():
    def __init__(self,ID):
        self.SGDID = ID
        self.input_nodes = [node for node in ID2input_dict[ID] if node != ID]
        self.status = 0

def get_other2ID():
    _other2ID = {}
    for row in C.execute("SELECT * FROM other2ID"):
        _other2ID[row[0]] = row[1]
    return _other2ID

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

def group_interact(group):
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

def init():
    Coon = sqlite3.connect("/Users/bingwang/VimWork/db/Scer.db")
    C = Coon.cursor()
    other2ID = get_other2ID()
    ID2input_dict = get_ID2Interact()
    slim_P_dict = {}
    slim_C_dict = {}
    slim_F_dict = {}
    GOID2group = {}
    SGDID2GO = {}
    #TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)
    for row in C.execute("SELECT SGDID,GOID,GO_Term,GO_Aspect FROM ID2GO WHERE slim = 1"):
        if row[3] == "P":
            if row[1] not in slim_P_dict:
                slim_P_dict[row[1]] = row[2]
        if row[3] == "C":
            if row[1] not in slim_C_dict:
                slim_C_dict[row[1]] = row[2]
        if row[3] == "F":
            if row[1] not in slim_F_dict:
                slim_F_dict[row[1]] = row[2]
        if row[1] not in GOID2group:
            GOID2group[row[1]] = []
        GOID2group[row[1]].append(row[0])
        if row[0] not in SGDID2GO:
            SGDID2GO[row[0]] = []
        SGDID2GO[row[0]].append(row[1])
    GO2interact = {}
    for GOID_1 in GOID2group:
        if GOID_1 not in GO2interact:
            GO2interact[GOID_1] = {}
        for ID in GOID2group[GOID_1]:
            for GOID_2 in SGDID2GO[ID]:
                if GOID_2 not in GO2interact[GOID_1]:
                    GO2interact[GOID_1][GOID_2] = 0
                GO2interact[GOID_1][GOID_2] += 1
    net_structure = [slim_P_dict,slim_C_dict,slim_F_dict,GOID2group,SGDID2GO,GO2interact]
    encode = json.dumps(net_structure)
    f = open("/Users/bingwang/VimWork/BioNetWork/net_structure","w")
    f.write(encode)
    f.close()

def G_init(slim_dict,slim):
    def check_field(pos,G,rate):
        for node in G:
            node_pos = G.node[node]["pos"]
            if math.sqrt(np.sum((pos-node_pos)**2)) < rate:
                return True
        return False

    if len(slim_dict) < 25:
        rate = 0.42
    elif len(slim_dict) < 42:
        rate = 0.3
    else:
        rate = 0.25

    G = nx.Graph()
    for node in slim_dict:
        pos = np.array((0.0,0.0))
        while check_field(pos,G,rate):
            pos = np.array((2.8*random.random()-1.4, 2.8*random.random()-1.4))
        G.add_node(node,size=len(GOID2group[node]),color=0,pos=pos)
    for node in G:
        G.node[node]["sum"] = 0
        G.node[node]["1"] = 0
        G.node[node]["2"] = 0
    for GOID_1 in slim_dict:
        for GOID_2 in GO2interact[GOID_1]:
            if GOID_2 != GOID_1 and GOID_2 in slim_dict:
                G.add_edge(GOID_1,GOID_2,weight=GO2interact[GOID_1][GOID_2],percent=0.5,percent_1=0.5,percent_2=0.5)
    png = "/Users/bingwang/VimWork/BioNetWork/slim_"+slim+".png"
    G = nx.relabel_nodes(G,slim_dict)
    nx.write_gpickle(G,"/Users/bingwang/VimWork/BioNetWork/G_slim_"+slim)
    draw_G(G,png)

def better_display(G,slim,fit=None):
    import engine.Genetic as Genetic
    _fit = "C" if fit == None else "L"
    R = Genetic.genetic(G,_fit)
    for node in G:
        G.node[node]["pos"] = R[node]
    nx.write_gpickle(G,"/Users/bingwang/VimWork/BioNetWork/G_slim_"+slim+"_"+_fit)

def draw_G(G,pngname,with_labels=None):
    draw_active = "1" 
    Pos = nx.get_node_attributes(G,'pos')
    node_size = []
    node_active_1 = []
    node_active_2 = []
    node_active_sum = []
    for node in G:
        size = math.log(G.node[node]["size"],2)*7500/len(G)
        node_size.append(size)
        node_active_1.append(G.node[node]["1"])
        node_active_2.append(G.node[node]["2"])
        node_active_sum.append(G.node[node]["sum"])
    if draw_active == "1":
        nx.draw_networkx_nodes(G,Pos,node_size=node_size,node_color=node_active_1,\
                cmap=plt.cm.Reds_r,alpha=0.6)
    elif draw_active == "2":
        nx.draw_networkx_nodes(G,Pos,node_size=node_size,node_color=node_active_2,\
                cmap=plt.cm.Greens_r,alpha=0.6)
    else:
        nx.draw_networkx_nodes(G,Pos,node_size=node_size,node_color=node_active_sum,\
                cmap=plt.cm.gray,alpha=0.6)
    for edge in G.edges():
        width = math.log(G[edge[0]][edge[1]]["weight"],2)
        if draw_active == "1":
            percent = G[edge[0]][edge[1]]["percent_1"]
        elif draw_active == "2":
            percent = G[edge[0]][edge[1]]["percent_2"]
        else: 
            percent = G[edge[0]][edge[1]]["percent"]
        nx.draw_networkx_edges(G,Pos,edgelist=[edge],width=width,alpha=percent)
    if with_labels == True:
        nx.draw_networkx_labels(G,Pos,font_size=10)
    plt.xlim(-2,1.9)
    plt.ylim(-1.7,1.6)
    plt.axis('off')
    plt.savefig(pngname,dpi=200)
    plt.clf()

def modify_G(G=None,G_pickle=None,slim_dict=None,node_size=None,node_pos=None,edge_width=None,\
        node_status_1=None,node_status_2=None,edge_active=None):
    if G == None and G_pickle == None:
        print "ERROR: G or G_pickle should provided"
        return None
    if G == None:
        G = nx.read_gpickle(G_pickle)
    if slim_dict != None:
        G.graph["slim"] = slim_dict
    if node_size != None:
        for node in G:
            G.node[node]["size"] = node_size[node]
    if node_pos != None:
        for node in G:
            G.node[node]["pos"] = node_pos[node]
    if edge_width != None:
        for node_1 in G:
            for node_2 in G[node_1]:
                G[node_1][node_2]["weight"] = edge_width[node_1][node_2]
    if node_status_1 != None:
        for node in G:
            G.node[node]["1"] = node_status_1[node]
    if node_status_2 != None:
        for node in G:
            G.node[node]["2"] = node_status_2[node]
    if edge_active != None:
        for node_1 in G:
            for node_2 in G[node_1]:
                G[node_1][node_2]["percent"] = edge_active[node_1][node_2]
                # a float between[0,1]
    if G == None:
        nx.write_gpickle(G,G_pickle)
    #png = "/Users/bingwang/VimWork/BioNetWork/slim_"+G.graph["slim"]+".png"
    #draw_G(G,png)
    return G

def get_input(CID):
    f = open("/Users/bingwang/VimWork/BioNetWork/ScerMicro_b.tab")
    SGDID_list = f.readline().split("\t")[1:-1] #because nothing after the last '\t'
    input_dict = {}
    for line in f:
        if line.startswith(CID):
            for i,num in enumerate(line.split("\t")[1:-1]):
                input_dict[SGDID_list[i]] = num
            f.close()
            return input_dict
    print "CID not find"
    return None

def calculate(input_dict,G):
    for GOID in G:
        G.node[GOID]["1"] = 0
        G.node[GOID]["2"] = 0
        for SGDID in GOID2group[GOID]:
            if SGDID not in input_dict:
                continue
            if input_dict[SGDID] == '1':
                G.node[GOID]["1"] += 1
            if input_dict[SGDID] == '2':
                G.node[GOID]["2"] += 1
        G.node[GOID]["1"] = 1-G.node[GOID]["1"] * 1.0 / G.node[GOID]['size']
        G.node[GOID]["2"] = 1-G.node[GOID]["2"] * 1.0 / G.node[GOID]['size']
        G.node[GOID]["sum"] = 1-(G.node[GOID]["1"]+G.node[GOID]["2"])*1.0/G.node[GOID]['size']
    
    for node_1 in G:
        for node_2 in G[node_1]:
            G[node_1][node_2]["percent"] = 0
            G[node_1][node_2]["percent_1"] = 0
            G[node_1][node_2]["percent_2"] = 0
    
    for SGDID in input_dict:
        if SGDID not in SGDID2GO or input_dict[SGDID] == '0':
            continue
        for node_1 in SGDID2GO[SGDID]:
            if node_1 not in G:
                continue
            for node_2 in SGDID2GO[SGDID]:
                if node_2 != node_1 and node_2 in G:
                    G[node_1][node_2]["percent"] += 0.49 / G[node_1][node_2]["weight"]
                    if input_dict[SGDID] == "1":
                        G[node_1][node_2]["percent_1"] += 0.49 / G[node_1][node_2]["weight"]
                    if input_dict[SGDID] == "2":
                        G[node_1][node_2]["percent_2"] += 0.49 / G[node_1][node_2]["weight"]
    return G


def draw_dicts(G):
    dicts_file = "/Users/bingwang/VimWork/BioNetWork/P_test/dict_list.txt"
    f = open(dicts_file)
    line_1 = f.readline().split("\t")[:-1]
    input_dicts = []
    for line in f:
        input_dict = {}
        for i,value in enumerate(line.split("\t")[:-1]):
            input_dict[line_1[i]] = value
        input_dicts.append(input_dict)

    for i,input_dict in enumerate(input_dicts):
        G = calculate(input_dict,G)
        png = "/Users/bingwang/VimWork/BioNetWork/P_test/slim_P_"+str(i)+".png"
        draw_G(G,png)


f = open("/Users/bingwang/VimWork/BioNetWork/net_structure")
encode = f.read()
[slim_P_dict,slim_C_dict,slim_F_dict,GOID2group,SGDID2GO,GO2interact] = json.loads(encode)
#G_init(slim_C_dict,"C")
G_pic = "/Users/bingwang/VimWork/BioNetWork/G_slim_C"
G = nx.read_gpickle(G_pic)
better_display(G,"C",fit="L")
'''
input_dict = get_input("10586882_0_1")
G = calculate(input_dict,G)
png = "/Users/bingwang/VimWork/BioNetWork/P_test/10586882_0_1.png"
draw_G(G,png)
'''
#draw_dicts()

