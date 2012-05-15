#coding:utf-8
import os
import math
import sqlite3

M_coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
M_c = M_coon.cursor()
#M_c.execute("CREATE TABLE PMID2readme (PMID,README)")
#M_c.execute("CREATE TABLE CID2condition (CID,condition)")
#M_c.execute("CREATE TABLE microarray (SGDID,CID,EXP,EXP_bool)")
other2ID = {}
for row in M_c.execute("SELECT * FROM other2ID"):
    other2ID[row[0]] = row[1]
'''
Microarray_Path = "/Users/bingwang/VimWork/db/Microarray/archive/"
f = open(Microarray_Path+"README")
PMID = f.readline()[1:].strip()
string = ""
for line in f:
    if line[0] == ">":
        M_c.execute("INSERT INTO PMID2readme VALUES (?,?)",(PMID,string))
        PMID = line[1:].strip()
        string = ""
    else:
        string += line

pclfiles = [name for name in os.listdir(Microarray_Path) if name.endswith(".pcl")]
for i,filename in enumerate(pclfiles):
    PMID = filename.split(".")[0]
    f = open(Microarray_Path+filename)
    conditions = f.readline().strip().split("\t")[3:]
    for j,condition in enumerate(conditions):
        M_c.execute("INSERT INTO CID2condition VALUES (?,?)",(PMID+"_"+str(j),condition))
    f.readline()
    for line in f:
        elements = line.replace("\n","").replace("\r","").split("\t")
        if len(elements[3:]) != len(conditions):
            print "check "+PMID+" gene "+elements[0]+" column seems not right"
            continue
        try:
            SGDID = other2ID[elements[0]]
        except:
            continue
        for k,value in enumerate(elements[3:]):
            CID = PMID+"_"+str(k)
            try:
                if float(value) >= 1:
                    value_bool = 1
                elif float(value) <= -1:
                    value_bool = -1
                elif -1< float(value) <1:
                    value_bool = 0
                elif math.isnan(float(value)):
                    value_bool = "nan"
                else:
                    print value
            except:
                if value != "":
                    print value
                value_bool = float("nan")
            M_c.execute("INSERT INTO microarray VALUES (?,?,?,?)",(SGDID,CID,value,value_bool))
    print filename+" finished!  "+str((i+1)*1.0/len(pclfiles))+"% done!"
#M_coon.commit()
'''
