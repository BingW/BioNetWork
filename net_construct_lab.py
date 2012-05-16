#conding:utf-8
import numpy as np
import time

def calculate_function(gene):
    def bayes_two_nodes():
        M_array = np.zeros((8133,3),dtype = np.int8)
        M_array[:,0] = line_0 
        M_array[:,1] = line_1 
        M_array[:,2] = line_2
        count_array = np.zeros((3,2,2),dtype = np.uint16)
        for line in M_array:
            if 99 in line or line[1] == 0 or line[2] == 0:
                continue
            else:
                count_array[line[0],line[1]-1,line[2]-1] += 1
        return count_array
  
    def bayes_one_nodes():
        M_array = np.zeros((8133,2),dtype = np.int8)
        M_array[:,0] = line_0 
        M_array[:,1] = line_1
        count_array = np.zeros((3,2),dtype = int)
        for line in M_array:
            if 99 in line or line[1] == 0:
                continue
            else:
                count_array[line[0],line[1]-1] += 1
        return count_array

    node_0 = gene.SGDID
    line_0 = Microarray[:,SGDID_list.index(node_0)]
    input_nodes = gene.input_nodes
    similar_percent = 0.95
    minimal_sum = 20 #P_value < 10^-7
    func = ""
    for i,node_1 in enumerate(input_nodes):
        line_1 = Microarray[:,SGDID_list.index(node_1)]
        count_array = bayes_one_nodes()
        cord_1 = count_array.argmax(axis=0)
        sum_1 = count_array.sum(axis=0)
        percent_1 = count_array.max(axis=0)*1.0/(sum_1+0.01)
        one_flag = 0
        for i_m,m in enumerate(cord_1):
            if sum_1[i_m] > minimal_sum and percent_1[i_m] > similar_percent:
                cond = node_1+"\t"+str(i_m)+"\t=>\t"+node_0+"\t"+str(m)+\
                        "\tconfi:\t"+str(percent_1[i_m])+"\n"
                func += cond
                one_flag = 1
                print cond.strip()
        if one_flag == 1:
            continue
        for node_2 in input_nodes[i+1:]:
            line_2 = Microarray[:,SGDID_list.index(node_2)]
            count_array = bayes_two_nodes()
            cord_2 = count_array.argmax(axis=0)
            sum_2 = count_array.sum(axis=0)
            percent_2 = count_array.max(axis=0)*1.0/(sum_2+0.01)
            #to escape conditions where sum = 0
            for i_m,m in enumerate(cord_2):
                for j_n,n in enumerate(m):
                    if sum_2[i_m,j_n] > minimal_sum and percent_2[i_m,j_n] > similar_percent:
                        cond = node_1+"\t"+str(i_m+1)+"\tAND\t"+node_2+"\t"+str(j_n+1)+\
                                "\t=>\t"+node_0+"\t"+str(n)+\
                                "\tconfi:\t"+str(percent_2[i_m,j_n])+"\n"
                        func += cond
                        print cond.strip()
    return func

class gene_node():
    def __init__(self,ID):
        self.SGDID = ID
        self.input_nodes = [node for node in ID2input_dict[ID] if node != ID
                and node in SGDID_list]
        self.status = 0

####################
####    main    ####
####################
lab_dict = "/Users/bingwang/VimWork/BioNetWork/"
s = "2300_2400"

f = open(lab_dict+"SGD_features.tab")
other2ID = {}
#other2ID[other] = ID
for line in f:
    elements = line.split("\t")
    try:
        other2ID[elements[0]]
        other2ID[elements[3]]
        other2ID[elements[4]]
        for name in elements[5].split("\t"):
            other2ID[name]
        for name in elements[8].split("\t"):
            other2ID[name]
        print "ID:",elements[0],"exist @:",other2ID[elements[0]]
    except:
        other2ID[elements[0]] = elements[0]
        other2ID[elements[3]] = elements[0]
        other2ID[elements[4]] = elements[0]
        for name in elements[5].split("\t"):
            other2ID[name] = elements[0]
        for name in elements[8].split("\t"):
            other2ID[name] = elements[0]
f.close()

f = open(lab_dict+"interaction_data.tab")
ID2input_dict = {}
#ID2input_dict[ID_B][ID_H] = True 
for line in f:
    elements = line.split("\t")
    inter_type = "G" if elements[5] == "genetic interactions" else "P"
    if elements[0] in other2ID and elements[2] in other2ID:
        ID_B = other2ID[elements[0]]
        ID_H = other2ID[elements[2]]
    else:
        print elements[0], "or", elements[1],"doesn't exist"
    if ID_B not in ID2input_dict:
        ID2input_dict[ID_B] = {}
    if ID_H not in ID2input_dict[ID_B]:
        ID2input_dict[ID_B][ID_H] = True
    if ID_H not in ID2input_dict:
        ID2input_dict[ID_H] = {}
    if ID_B not in ID2input_dict[ID_H]:
        ID2input_dict[ID_H][ID_B] = True
f.close()
print "ID2input_dict init finish!"

f = open(lab_dict+"ScerMicro_b.tab")
SGDID_list = f.readline().split("\t")[1:-1] #because nothing after the last '\t'
Microarray = np.zeros((8133,len(SGDID_list)),dtype = np.uint8)
for i,line in enumerate(f):
    elements = line.split("\t")[:-1] #because nothing after the last '\t'
    for j,num in enumerate(elements[1:]):
        Microarray[i,j] = num
    if i%20 == 0:
        print "loding Microarray "+str(round(i*100.0/8134,2))+"%"
f.close()
print "Microarray init finish!"

temp_list = SGDID_list[int(s.split("_")[0]):int(s.split("_")[1])]
total = 0
for i,node in enumerate(temp_list):
    if node in ID2input_dict:
        gene = gene_node(node)
        total += len(gene.input_nodes) ** 2
    else:
        print "node lack data "+node

f = open(lab_dict+"system_"+s+".tab","w")
time_start = time.time()
finished = 0
for node in temp_list:
    if node in ID2input_dict:
        gene = gene_node(node)
        print "writing system_"+s+".tab"
        print "Scaning...",node
        print "\tGroups:\t",len(gene.input_nodes)
        system = calculate_function(gene)
        f.write(system)
        time_used = time.time() - time_start
        finished += len(gene.input_nodes) ** 2
        finish_p = round(finished*1.0/total,4)
        print finish_p*100,"% finished!"
        print "time used:", \
            int(time_used/3600),"h", \
            int((time_used%3600)/60),"min",\
            int((time_used%3600)%60),"s"
        print "time left:", \
            int((time_used/finish_p-time_used)/3600),"h", \
            int(((time_used/finish_p-time_used)%3600)/60),"min",\
            int(((time_used/finish_p-time_used)%3600)%60),"s"


