#coding:utf-8
import os
import math
import sqlite3

Coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
C = Coon.cursor()
#TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)
other2ID = {}
for row in C.execute("SELECT * FROM other2ID"):
    other2ID[row[0]] = row[1]

ID_sum = []
for row in C.execute("SELECT SGDID FROM ID2GO"):
    if row[0] not in ID_sum:
        ID_sum.append(row[0])

#g = open("/Users/bingwang/VimWork/db/ScerMicro.tab","w")
g = open("/Users/bingwang/VimWork/db/ScerMicro_b.tab","w")
g.write("\t")
for SGDID in ID_sum:
    g.write(SGDID+"\t")
g.write("\n")
Microarray_Path = "/Users/bingwang/VimWork/db/Microarray/archive/"
pclfiles = [name for name in os.listdir(Microarray_Path) if name.endswith(".pcl")]

for i,filename in enumerate(pclfiles):
    PMID = filename.split(".")[0]
    f = open(Microarray_Path+filename)
    conditions = f.readline().split("\t")[3:]
    CID_dict = [PMID+"_"+str(j) for j in range(len(conditions))]
    f.readline()
    M_dict = {}
    for line in f:
        elements = line.replace("\n","").replace("\r","").split("\t")
        if len(elements[3:]) != len(conditions):
            print "check "+PMID+" gene "+elements[0]+" column seems not right"
            continue
        try:
            SGDID = other2ID[elements[0]]
            M_dict[SGDID] = {}
        except:
            continue
        for k,value in enumerate(elements[3:]):
            CID = PMID+"_"+str(k)
            try:
                value = float(value)            
            except:
                value = float("nan")
            M_dict[SGDID][CID] = value
    for CID in CID_dict:
        g.write(CID+"\t")
        for SGDID in ID_sum:
            if SGDID not in M_dict:
                g.write("99\t")
            else:
                #g.write(str(round(M_dict[SGDID][CID],2))+"\t")
                if M_dict[SGDID][CID] >= 1:
                    g.write("1\t")
                elif M_dict[SGDID][CID] <= -1:
                    g.write("2\t")
                elif -1 < M_dict[SGDID][CID] < 1:
                    g.write("0\t")
                else:
                    g.write("99\t")
        g.write("\n")
    print filename+" finished!  "+str((i+1)*1.0/len(pclfiles))+"% done!"
