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
    return right * 1.0 / (len(compare_list) - NA)

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

def predict_series(init_dict,out_file,real_dicts,step):
    f = open(out_file,"w")
    predict_dict = Run(init_dict,LAW)
    for node in ALL_nodes:
        f.write(node+"\t")
    f.write("\n")
    for node in ALL_nodes:
        f.write(str(init_dict[node])+"\t")
    f.write("\n")
    for node in ALL_nodes:
        f.write(str(predict_dict[node])+"\t")
    f.write("\n")
    zero_dict = {}
    for node in ALL_nodes:
        zero_dict[node] = 0
    for i in xrange(step):
        predict_dict = Run(predict_dict,LAW)
        for real_dict in real_dicts:
            print CID,compare(predict_dict,real_dict,ALL_nodes),\
                    compare(zero_dict,real_dict,ALL_nodes)
        for node in ALL_nodes:
            f.write(str(predict_dict[node])+"\t")
        f.write("\n")

def write_real_series(series_data,out_file):
    f = open(out_file,"w")
    for node in ALL_nodes:
        f.write(node+"\t")
    f.write("\n")
    for node_dict in series_data:
        for node in ALL_nodes:
            f.write(str(node_dict[node])+"\t")
        f.write("\n")

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
    _99 = _99 *100.0 / len(compare_list)
    print "0:",round(status[0],4),"%  1:",round(status[1],4),\
            "%  2:",round(status[2],4),"%  99:",round(_99,4),"%"

#########main###########
'''
LAW,referenced = LAW_init()
ALL_nodes = [node for node in LAW]
s_nodes = [node for node in referenced if node not in LAW]
f_nodes = [node for node in LAW if node not in referenced]
for node in s_nodes:
    ALL_nodes.append(node)

'''
#CID_list = ["10586882_0_0","10586882_0_1","10586882_0_2","10586882_0_3",\
#        "10586882_0_4","10586882_0_5","10586882_0_6"]
#CID_list = ["10611304_0_0","10611304_0_1","10611304_0_2","10611304_0_3",\
#        "10611304_0_4"]
CID_list = ["9843569_1_0","9843569_1_1","9843569_1_2","9843569_1_3","9843569_1_4",\
        "9843569_1_5","9843569_1_6","9843569_1_7","9843569_1_8","9843569_1_9", \
        "9843569_1_10","9843569_1_11","9843569_1_12","9843569_1_13","9843569_1_14",\
        "9843569_1_15","9843569_1_16","9843569_1_17","9843569_1_18","9843569_1_19",
        "9843569_1_20","9843569_1_21","9843569_1_22","9843569_1_23","9843569_1_24"]
series_data = [get_input(CID) for CID in CID_list]
real_file = path+"results/real_9843569_1.txt"
write_real_series(series_data,real_file)
predict_one_file = path+"results/predict_9843569_1_1.txt"
#predict_file = path+"results/predict_10611304_0.txt"
#predict_series(series_data[0],predict_file,series_data,1000)
def predict_one(ref_dict,out_file):
    count_status(ref_dict,ALL_nodes)
    predict_dict = {}
    for node in ALL_nodes:
        if node in s_nodes and node in ref_dict:
            predict_dict[node] = ref_dict[node]
        else:
            predict_dict[node] = 99
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
        for node in ALL_nodes:
            f.write(str(predict_dict[node])+"\t")
        f.write("\n")
    predict_dict = dict_average(all_dicts)
    print compare(predict_dict,ref_dict,ALL_nodes)
predict_one(series_data[1],predict_one_file)
