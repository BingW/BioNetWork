#coding:utf-8
import os
import sqlite3
import numpy as np
import random
path = "/Users/bingwang/VimWork/BioNetWork/"
def LAW_init():
    LAW = {}
    referenced = []
    f = open(path+"system_data")
    for line in f:
        elements = line.split("\t")
        if len(elements) == 10:
            if elements[6] not in LAW:
                LAW[elements[6]] = {}
                LAW[elements[6]]["1"] = []
                LAW[elements[6]]["0"] = []
                LAW[elements[6]]["2"] = []
            LAW[elements[6]][elements[7]].append((elements[0],elements[1],elements[3],elements[4]))
            referenced.append(elements[6])
            referenced.append(elements[0])
            referenced.append(elements[3])
        elif len(elements) == 7:
            if elements[3] not in LAW:
                LAW[elements[3]] = {}
                LAW[elements[3]]["1"] = []
                LAW[elements[3]]["0"] = []
                LAW[elements[3]]["2"] = []
            LAW[elements[3]][elements[4]].append((elements[0],elements[1]))
            referenced.append(elements[3])
            referenced.append(elements[0])
        else:
            print line
    return LAW, set(referenced)

def Run(input_dict,referenced,LAW):
    population = 1
    colony = []
    def check_condition(condition):
        if len(condition) == 2:
            return True if input_dict[condition[0]] == condition[1] else False
        if len(condition) == 4:
            return True if input_dict[condition[0]] == condition[1] and \
                    input_dict[condition[2]] == condition[3] else False
    for i in range(population):
        out_dict = {}
        for node in LAW:
            node_status = input_dict[node]
            if node_status == '99':
                continue
            status_dict = {}
            for status in ["1","2","0"]:
                status_dict[status] = 0
                for condition in LAW[node][status]:
                    if check_condition:
                        status_dict[status] += 1
            if status_dict[node_status] > 0 and random.random() < 0.8:
                out_dict[node] = node_status
            sum_status = status_dict["0"]+status_dict["1"]+status_dict["2"]
            if sum_status == 0:
                out_dict[node] = node_status
            randint = random.randint(0,sum_status)
            if randint < status_dict["0"]:
                out_dict[node] = "0"
            elif randint < status_dict["0"]+status_dict["1"]:
                out_dict[node] = "1"
            elif randint < status_dict["0"]+status_dict["1"]+status_dict["2"]:
                out_dict[node] = "2"

        length = len(out_dict)
        for node in referenced:
            if node not in out_dict:
                out_dict[node] = input_dict[node]
        colony.append(out_dict)
    best = 0
    best_index = 0
    for i,pop in enumerate(colony):
        score = len([node for node in pop if pop[node]=='0'])
        if score > best:
            best = score
            best_index = i
    print best,"/",length
    return colony[best_index]

def compare(dict_predict,dict_target,compare_list):
    right = 0
    for node in compare_list:
        if dict_predict[node] == dict_target[node]:
            right += 1
    return right * 1.0 / len(compare_list)

def get_input(CID):
    f = open(path+"ScerMicro_b.tab")
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

series_data = {}
CID_list = ["10586882_0_0","10586882_0_1","10586882_0_2","10586882_0_3","10586882_0_4","10586882_0_5","10586882_0_6"]
for CID in CID_list:
    series_data[CID] = get_input(CID)

LAW,referenced = LAW_init()
input_dict = series_data["10586882_0_0"]

ALL_node = [node for node in LAW]
for node in [n for n in referenced if n not in LAW]:
    ALL_node.append(node)

f = open(path+"P_test/dict_list.txt","w")
for node in ALL_node:
    f.write(node+"\t")
f.write("\n")
for CID in CID_list:
    for node in ALL_node:
        f.write(series_data[CID][node]+"\t")
    f.write("\n")

old = [input_dict]
zero_dict = {}
for node in ALL_node:
    zero_dict[node] = "0"
for i in range(100):
    input_dict = Run(input_dict,referenced,LAW)
    for CID in CID_list:
        print CID,compare(input_dict,series_data[CID],ALL_node),\
                compare(zero_dict,series_data[CID],ALL_node)
    if input_dict in old:
        break
    for node in ALL_node:
        f.write(input_dict[node]+"\t")
    f.write("\n")
    old.append(input_dict)


