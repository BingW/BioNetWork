#coding:utf-8
import os
import sqlite3
import numpy as np
import random
import json
import array
path = "/Users/bingwang/VimWork/BioNetWork/"
def LAW_init():
    LAW = {}
    referenced = []
    f = open(path+"results/system_data")
    for line in f:
        elements = line.strip().split("\t")
        if len(elements) == 10:
            if elements[6] not in LAW:
                LAW[elements[6]] = {}
                LAW[elements[6]][1] = []
                LAW[elements[6]][0] = []
                LAW[elements[6]][2] = []
            LAW[elements[6]][int(elements[7])].append((elements[0],int(elements[1]),elements[3],int(elements[4])))
            referenced.append(elements[6])
            referenced.append(elements[0])
            referenced.append(elements[3])
        elif len(elements) == 7:
            if elements[3] not in LAW:
                LAW[elements[3]] = {}
                LAW[elements[3]][1] = []
                LAW[elements[3]][0] = []
                LAW[elements[3]][2] = []
            LAW[elements[3]][int(elements[4])].append((elements[0],int(elements[1])))
            referenced.append(elements[3])
            referenced.append(elements[0])
        else:
            print line
    return LAW, list(set(referenced))

def Run(init_dict,LAW):
    def calculate_status():
        status = np.zeros([3])
        for node in init_dict:
            if status_dict[node] == 99:
                continue
            else:
                status[init_dict[node]] += 1
   
    def check_condition(condition):
        if len(condition) == 2:
            return True if init_dict[condition[0]] == condition[1] else False
        if len(condition) == 4:
            return True if init_dict[condition[0]] == condition[1] and \
                    init_dict[condition[2]] == condition[3] else False
    out_dict = {}
    for node in ALL_nodes:
        node_status = init_dict[node]
        if node not in LAW:
            out_dict[node] = node_status
            continue
        status_dict = array.array('i',[0,0,0]) 
        for status in xrange(3):
            for condition in LAW[node][status]:
                if check_condition(condition):
                    status_dict[status] += 1
        if node_status != 99 and status_dict[node_status] > 0 and random.random() < 0.8:
            out_dict[node] = node_status
        sum_status = np.sum(status_dict)
        if sum_status == 0:
            out_dict[node] = node_status
            continue
        randint = random.randint(0,sum_status)
        if randint < status_dict[0]:
            out_dict[node] = 0
        elif randint < np.sum(status_dict[0:2]):
            out_dict[node] = 1
        else:
            out_dict[node] = 2
    return out_dict

def compare(dict_predict,dict_target,compare_list):
    right = 0
    NA = 0
    for node in compare_list:
        if dict_target[node] == 99:
            NA += 1
        elif dict_predict[node] == dict_target[node]:
            right += 1
    return round(right * 1.0 / (len(compare_list) - NA),4)

def get_input(CID):
    f = open(path+"results/ScerMicro_b.tab")
    SGDID_list = f.readline().split("\t")[1:-1] #because nothing after the last '\t'
    input_dict = {}
    for line in f:
        if line.startswith(CID):
            for i,num in enumerate(line.split("\t")[1:-1]):
                input_dict[SGDID_list[i]] = int(num)
            f.close()
            return input_dict
    print "CID not find"
    return None

def predict_series(init_dict,step,real_CIDs=None,out_file=None):
    if real_CIDs != None:
        real_dicts = [get_input(CID) for CID in real_CIDs]
        best_match = {}
        for i,status_dict in enumerate(real_dicts):
            print CID_list[i]+"\t"+str(compare(status_dict,real_dicts[0],s_nodes))+\
                    "\t"+str(calculate_balance(status_dict))
            best_match[CID_list[i]] = (compare(real_dicts[0],status_dict,ALL_nodes),0)
        for CID in real_CIDs:
            print CID, best_match[CID]
        write_real_series(real_dicts,out_file+".real")

    predict_dict = Run(init_dict,LAW)
    if out_file != None:
        f = open(out_file+".predict","w")
        for node in ALL_nodes:
            f.write(node+"\t")
        f.write("\n")
        for node in ALL_nodes:
            f.write(str(init_dict[node])+"\t")
        f.write("\n")
        for node in ALL_nodes:
            f.write(str(predict_dict[node])+"\t")
        f.write("\n")

    for i in xrange(step):
        predict_dict = Run(predict_dict,LAW)
        if real_CIDs != None:
            for j,real_dict in enumerate(real_dicts):
                score = compare(predict_dict,real_dict,ALL_nodes)
                if score > best_match[CID_list[j]][0]:
                    best_match[CID_list[j]] = (score,i)
                    print CID_list[j]+"\t"+str(score)+"\t"+str(i+1)

        if out_file != None:
            for node in ALL_nodes:
                f.write(str(predict_dict[node])+"\t")
            f.write("\n")
    if real_dict != None:
        return best_match

def write_real_series(series_data,out_file):
    if type(series_data) == type([]):
        f = open(out_file,"w")
        for node in ALL_nodes:
            f.write(node+"\t")
        f.write("\n")
        for node_dict in series_data:
            for node in ALL_nodes:
                f.write(str(node_dict[node])+"\t")
            f.write("\n")
    else:
        print "Type Error"
        return None

def dict_average(dicts):
    avg_dict = {}
    for node in dicts[0]:
        status_dict = array.array('i',[0,0,0]) 
        for pre_dict in dicts:
            if pre_dict[node] != 99:
                status_dict[pre_dict[node]] += 1
        avg_dict[node] = status_dict.index(max(status_dict))
    return avg_dict

def count_status(status_dict,compare_list):
    status = np.zeros([3])
    _99 = 0
    for node in compare_list:
        if status_dict[node] == 99:
            _99 += 1
        else:
            status[status_dict[node]] += 1
    status = 100 * status / len(compare_list)
    _99 = _99 * 100.0 / len(compare_list)
    print "0:",round(status[0],4),"%  1:",round(status[1],4),\
            "%  2:",round(status[2],4),"%  99:",round(_99,4),"%"
    return round(status[0],4)

def calculate_balance(status_dict):
    status = np.zeros([3])
    _99 = 0
    for node in status_dict:
        if status_dict[node] == 99:
            _99 += 1
        else:
            status[status_dict[node]] += 1
    status = status / len(status_dict)
    _99 = _99 / len(status_dict)
    return round(status[0],4)

def predict_one(ref_dict,out_file = None):
    count_status(ref_dict,ALL_nodes)
    predict_dict = {}
    for node in ALL_nodes:
        if node in s_nodes and node in ref_dict:
            predict_dict[node] = ref_dict[node]
        else:
            predict_dict[node] = 99
    if out_file != None:
        f = open(out_file,"w")
        for node in ALL_nodes:
            f.write(node+"\t")
        f.write("\n")
        for node in ALL_nodes:
            f.write(str(predict_dict[node])+"\t")
        f.write("\n")
    print compare(predict_dict,ref_dict,ALL_nodes)
    all_dicts = [predict_dict]
    for i in xrange(10):
        predict_dict = Run(predict_dict,LAW)
        all_dicts.append(predict_dict)
        print compare(predict_dict,ref_dict,ALL_nodes)
        if out_file != None:
            for node in ALL_nodes:
                f.write(str(predict_dict[node])+"\t")
            f.write("\n")
    predict_dict = dict_average(all_dicts)
    all_dicts = [predict_dict]
    print compare(predict_dict,ref_dict,ALL_nodes)
    for i in xrange(10):
        predict_dict = Run(predict_dict,LAW)
        all_dicts.append(predict_dict)
        print compare(predict_dict,ref_dict,ALL_nodes)
        if out_file != None:
            for node in ALL_nodes:
                f.write(str(predict_dict[node])+"\t")
            f.write("\n")
    predict_dict = dict_average(all_dicts)
    print compare(predict_dict,ref_dict,ALL_nodes)
    return compare(predict_dict,ref_dict,ALL_nodes)

#####main###########
'''
LAW,referenced = LAW_init()
ALL_nodes = [node for node in LAW]
s_nodes = [node for node in referenced if node not in LAW]
f_nodes = [node for node in LAW if node not in referenced]
for node in s_nodes:
    ALL_nodes.append(node)

'''
M_coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
M_c = M_coon.cursor()
CID2Condition = {}
scores = []
for row in M_c.execute("SELECT * FROM CID2Condition"):
    CID2Condition[row[0]] = row[1]
for CID in CID2Condition:
    if "9843569_1" in CID:
        print CID,CID2Condition[CID]
'''
ID2Interact = {}
for row in M_c.execute("SELECT SGDID_1,SGDID_2,GP FROM ID2Interact"):
    if row[0] not in ID2Interact:
        ID2Interact[row[0]] = {}
    if row[1] not in ID2Interact:
        ID2Interact[row[1]] = {}
    if row[1] not in ID2Interact[row[0]]:
        ID2Interact[row[0]][row[1]] = row[2]
    if row[0] not in ID2Interact[row[1]]:
        ID2Interact[row[1]][row[0]] = row[2]

import json
f = open(path+"results/net_structure")
[slim_P_dict,slim_C_dict,slim_F_dict,GOID2group,SGDID2GO,GO2interact] = json.loads(f.read())
##############
# modurility #
##############
this_dict = slim_P_dict#slim_C_dict,slim_F_dict,GOID2group
this_dict = [GOID for GOID in this_dict]
groups = [GOID2group[GOID] for GOID in this_dict]
group_genes = []
overlap = []
for GOID_1 in this_dict:
    for GOID_2 in this_dict:
        if GOID_1 not in GO2interact or GOID_2 not in GO2interact[GOID_1]:
            overlap.append(0)
            continue
        over_p = GO2interact[GOID_1][GOID_2] * 1.0 / \
                (len(GOID2group[GOID_1])+len(GOID2group[GOID_2]))
        overlap.append(over_p)
print "overlap:", np.sum(overlap)/len(overlap) 

for group in groups:
    for gene in group:
        group_genes.append(gene)
group_genes = list(set(group_genes))
E_total = 0
gene_reuse_count = np.zeros([len(group_genes)])
for group in groups:
    for gene_1 in group:
        gene_reuse_count[group_genes.index(gene_1)] += 1
        if gene_1 not in ID2Interact:
            continue
        for gene_2 in ID2Interact[gene_1]:
            if gene_2 in group_genes:
                E_total += 1
print np.sum(gene_reuse_count)*1. /len(groups) /len(group_genes)

E_total = E_total / 2
print E_total
M = 0
E_total_2 = 0
for group in groups:
    E_c_in = 0
    E_c_out = 0
    for gene_1 in group:
        if gene_1 not in ID2Interact:
            continue
        for gene_2 in ID2Interact[gene_1]:
            if gene_2 not in group_genes:
                continue
            if gene_2 in group:
                E_c_in += 1
            else:
                E_c_out += 1
    E_total_2 += E_c_in
    if E_c_in%2 != 0:
        print E_c_in,"Error!"
    E_c_in = E_c_in / 2
    M += ((E_c_in * 1. / E_total) - ((2.*E_c_in+E_c_out)/(2.*E_total))**2)
    E_total_2 += E_c_out

print E_total_2/2,"should equal to",E_total
print "M = ",M


'''
