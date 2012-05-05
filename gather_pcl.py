#coding: utf-8
import os
import numpy
import math


def ID_initial():
    _f = open("/Users/bingwang/VimWork/db/SGD_features.tab")
    _other2ID = {}
    #other2ID[other] = ID
    _ID2Feature = {}
    #ID2Feature[ID] = [feature_name,stardand_name,Type,Description]
    for _line in _f:
        _elements = _line.split("\t")
        try:
            _other2ID[_elements[0]]
            _other2ID[_elements[3]]
            _other2ID[_elements[4]]
            for _name in _elements[5].split("\t"):
                _other2ID[_name]
            for _name in _elements[8].split("\t"):
                _other2ID[name]
            print "ID:",_elements[0],"exist @:",_other2ID[_elements[0]]
        except:
            _ID2Feature[_elements[0]] = [_elements[3],_elements[4],_elements[1],_elements[15].strip()]
            _other2ID[_elements[0]] = _elements[0]
            _other2ID[_elements[3]] = _elements[0]
            _other2ID[_elements[4]] = _elements[0]
            for _name in _elements[5].split("\t"):
                _other2ID[_name] = _elements[0]
            for _name in _elements[8].split("\t"):
                _other2ID[_name] = _elements[0]
    return _other2ID,_ID2Feature

def float_dict(_dict):
    _out = []
    for _num in _dict:
        try:
            _out.append(float(_num))
        except:
            _out.append(float("nan"))
    return _out

def log_transmit(in_dict):
    _avg = numpy.mean([_x for _x in in_dict if math.isnan(_x) == False])
    return [math.log((_x/_avg),2) for _x in in_dict]

def is_log_transmit(in_dict):
    _valid = [_x for _x in in_dict if math.isnan(_x) == False]
    if len(_valid) == 0:
        return None
    else:
        return True if min(_valid) < 0 else False

def check_file_log_status(filename):
    _f = open(filename)
    _f.readline()
    _f.readline()
    _flag = False
    for _i in range(20):
        _m_array = _f.readline().replace("\n","").replace("\r","").split("\t")[3:]
        if is_log_transmit(float_dict(_m_array)) == True:
            _flag = True
    return _flag

#in_file = "/Users/bingwang/VimWork/db/Microarray/Abbott_2008_PMID_18676708/GSE10066_setA_family.pcl"
#out_file = "/Users/bingwang/VimWork/test.pcl"
#in_dict = float_dict(["empty","4.1","4.2","4.0","3.9","3.7","3.9","3.8"])
#aft_log = log_transmit(in_dict)
#print in_dict
#print aft_log
#print is_log_transmit(in_dict)
#print is_log_transmit(aft_log)
Microarray_Path = "/Users/bingwang/VimWork/db/Microarray/"
other2ID,ID2Feature = ID_initial()
ID2Expression = {}
#ID2Expression[ID][condition] = experssion
condition2PMID = {}
PMID2Readme = {} 
for data_set in os.listdir(Microarray_Path):
    if data_set.count("PMID") == 0:
        continue
    PMID = data_set.split("_")[-1]
    f = open(Microarray_Path+data_set+"/README")
    PMID2Readme[PMID] = f.read()
    pclfiles = [pcl for pcl in os.listdir(Microarray_Path+data_set) if pcl.endswith(".pcl")]
    for i,pclfile in enumerate(pclfiles):
        if check_file_log_status(Microarray_Path+data_set+"/"+pclfile):
            try:
                open(Microarray_Path+"archave/"+PMID+"_"+i+".pcl")
            except:
                g = open(Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl","w")
                f = open(Microarray_Path+data_set+"/"+pclfile)
                g.write(f.read())
        else:
            try:
                open(Microarray_Path+"archave/"+PMID+"_"+i+".pcl")
            except:
                f = open(Microarray_Path+data_set+"/"+pclfile)
                g = open(Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl","w")
                g.write(f.readline())
                g.write(f.readline())
                for line in f:
                    m_array = line.replace("\n","").replace("\r","").split("\t")
                    for item in m_array[:3]:
                        g.write(item+"\t")
                    m_array = log_transmit(float_dict(m_array[3:]))
                    for num in m_array[:-1]:
                        g.write(str(num)+"\t")
                    g.write(str(m_array[-1])+"\n")
        

'''
        column = f.readline().strip().split("\t")
        f.readline() #skip GWEIGHT line
        for line in f:
            line = line.replace("\n","").replace("\r","") #DO NOT use strip()
            elements = line.split("\t")
            if elements[0] != "":
                PMID2Expression[PMID][i][elements[0]]=elements[3:]
            else:
                print line,"donot have name"
            break
        #print "/Users/bingwang/VimWork/db/Microarray_archive/PMID_"+PMID+"_"+str(i)+".pcl"
#print PMID2Readme["12058033"]
'''
