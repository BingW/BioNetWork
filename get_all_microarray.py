#coding:utf-8
microarray_path = "/Users/bingwang/VimWork/db/Microarray/"
import os
for filename in os.listdir(microarray_path):
    if "PMID" in filename:
        elements = filename.split("_")
        PMID = elements[-1]
        year = elements[-3]
        author = "_".join(elements[:-3])
        num = 0
        for M in os.listdir(microarray_path+filename):
            if M.endswith(".pcl"):
                f = open(microarray_path+filename+"/"+M)
                num += len(f.readline().split("\t")[3:])
        print PMID+"\t"+author+"\t"+year+"\t"+str(num)

        
        
       

