#conding:utf-8
import sqlite3
import numpy as np
import time
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

def draw_G(G,R,pngname,label):
        nx.draw(G,R,node_size=5,with_labels=label)
        plt.savefig(pngname,dpi=50)
        plt.clf()

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
'''
slim_P_dict = {}
slim_C_dict = {}
slim_F_dict = {}
GOID2group = {}
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

