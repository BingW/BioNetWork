#conding:utf-8
import sqlite3,time,random,math,json,os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
path = "/Users/bingwang/VimWork/BioNetWork/"
#TABLE CID2condition (CID,condition) #CID = PMID_index_cindex
#TABLE PMID2readme (PMID,README)
#TABLE other2ID (other unique, SGDID)
#TABLE microarray (SGDID,CID,EXP,EXP_bool)
#TABLE ID2Interact (SGDID_1, SGDID_2, GP, ExpType, Phenotype)
#TABLE ID2Feature (SGDID, feature, stardand, Type, Descrip)
#TABLE ID2Product (SGDID, product)
#TABLE ID2Phenotype (SGDID, mutan_type, phenotype, chemical, condition, details, reporter)
#TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)

def structure_init():
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
    f = open(path+"results/net_structure","w")
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
    png = path+"/results/slim_"+slim+"/slim_"+slim+".png"
    G = nx.relabel_nodes(G,slim_dict)
    nx.write_gpickle(G,path+"/results/G_slim_"+slim)
    draw_G(G,png)

def better_display(G,slim,pic,fit=None,pngpath=None,bw=None):
    import engine.Genetic as Genetic
    _fit = "C" if fit == "C" else "L"
    R = Genetic.genetic(G,_fit,pngpath,bw)
    for node in G:
        G.node[node]["pos"] = R[node]
    nx.write_gpickle(G,pic)

def draw_G(G,pngname,with_labels=None,draw_active=None):
    if with_labels==True:
        plt.figure(1,figsize=(10,6))
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
    elif draw_active == "sum":
        nx.draw_networkx_nodes(G,Pos,node_size=node_size,node_color=node_active_sum,\
                cmap=plt.cm.gray,alpha=0.6)
    else:
        nx.draw_networkx_nodes(G,Pos,node_size=node_size,node_color="white")
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
        node_dict = {}
        re_node_dict = {}
        for i,node in enumerate(G):
            node_dict[node] = i
            re_node_dict[i] = node
        G = nx.relabel_nodes(G,node_dict)
        new_Pos = {}
        for node in Pos:
            new_Pos[node_dict[node]] = Pos[node]
        s = ""
        if slim == "P":
            nx.draw_networkx_labels(G,new_Pos,font_size=7)
            for i in re_node_dict:
                s += " "*(2-len(str(i)))+str(i)+": "+re_node_dict[i]
                s += " "*(30-len(re_node_dict[i])) if len(re_node_dict[i]) < 30 else "  "
                if i%2 == 0:
                    s += "\n"
            plt.figtext(0.58,0.12,s,family="monospace",horizontalalignment='left',size="7")
        elif slim == "F":
            nx.draw_networkx_labels(G,new_Pos,font_size=8)
            for i in re_node_dict:
                s += " "*(2-len(str(i)))+str(i)+": "+re_node_dict[i]+"\n"
            plt.figtext(0.58,0.05,s,family="monospace",horizontalalignment='left',size="8")
        elif slim == "C":
            nx.draw_networkx_labels(G,new_Pos,font_size=10)
            for i in re_node_dict:
                s += " "*(2-len(str(i)))+str(i)+": "+re_node_dict[i]+"\n"
            plt.figtext(0.60,0.14,s,family="monospace",horizontalalignment='left',size="11")


    if with_labels == True:
        plt.xlim(-1.6,3.8)
    else:
        plt.xlim(-1.6,1.8)
    plt.ylim(-1.6,1.8)
    plt.axis('off')
    plt.savefig(pngname,dpi=400)
    plt.clf()

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
        G.node[GOID]["sum"] = 1-(G.node[GOID]["1"]+G.node[GOID]["2"]) * 1.0/G.node[GOID]['size']
    
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

def draw_dicts(G,dicts_file,pngpath):
    middle = 10 
    #os.system("mkdir "+pngpath+"1/")
    #os.system("mkdir "+pngpath+"2/")
    #os.system("mkdir "+pngpath+"sum/")
    f = open(dicts_file)
    line_1 = f.readline().split("\t")[:-1]
    input_dicts = []
    for line in f:
        input_dict = {}
        for i,value in enumerate(line.split("\t")[:-1]):
            input_dict[line_1[i]] = value
        input_dicts.append(input_dict)

    series = []
    for i,input_dict in enumerate(input_dicts):
        G = calculate(input_dict,G)
        series.append(G.copy())
    for i in xrange(len(series)-1):
        G_i = series[i]
        G_n = series[i+1]
        for j in xrange(middle):
            for node_1 in G:
                G.node[node_1]["1"] = G_i.node[node_1]["1"]+\
                        j*(G_n.node[node_1]["1"] - G_i.node[node_1]["1"])/middle
                G.node[node_1]["2"] = G_i.node[node_1]["1"]+\
                        j*(G_n.node[node_1]["2"] - G_i.node[node_1]["2"])/middle
                G.node[node_1]["sum"] = G_i.node[node_1]["1"]+\
                        j*(G_n.node[node_1]["sum"] - G_i.ndoe[node_1]["sum"])/middle
                for node_2 in G[node_1]:
                    G[node_1][node_2]["percent"] = G_i[node_1][node_2]["percent"]+\
                            j*(G_n[node_1][node_2]["percent"]-G_i[node_1][node_2]["percent"])/middle
                    G[node_1][node_2]["percent_1"] = G_i[node_1][node_2]["percent_1"]+\
                            j*(G_n[node_1][node_2]["percent_1"]-G_i[node_1][node_2]["percent_1"])/middle 
                    G[node_1][node_2]["percent_2"] = G_i[node_1][node_2]["percent_2"]+\
                            j*(G_n[node_1][node_2]["percent_2"]-G_i[node_1][node_2]["percent_2"])/middle 

            png = pngpath+"1/"+str(i*middle+j)+".png"
            draw_G(G,png,draw_part="1")
            png = pngpath+"2/"+str(i*middle+j)+".png"
            draw_G(G,png,draw_part="2")
            png = pngpath+"sum/"+str(i*middle+j)+".png"
            draw_G(G,png,draw_part="sum")

def unrelabel_G(G,slim_dict):
    relabel_dict = {}
    for node in slim_dict:
        relabel_dict[slim_dict[node]] = node
    G = nx.relabel_nodes(G,relabel_dict)
    return G

f = open(path+"results/net_structure")
[slim_P_dict,slim_C_dict,slim_F_dict,GOID2group,SGDID2GO,GO2interact] = json.loads(f.read())
slim = "F"
fitness = "C"
#pic_original = path+"results/slim_"+slim+"/G_slim_"+slim
pic_better =  path+"results/slim_"+slim+"/G_slim_"+slim+"_"+fitness
G = nx.read_gpickle(pic_better)
draw_G(G,path+"test.png",with_labels=True)
#CID = "10586882_0"
#CID = "10611304_0"
#CID = "9843569_1"
#fitness = "C"
#for slim in ["P","C","F"]:
#    G_pic= path+"results/slim_"+slim+"/G_slim_"+slim+"_"+fitness
#    G = nx.read_gpickle(G_pic)
#    if slim == "P":
#        G = unrelabel_G(G,slim_P_dict)
#    elif slim == "C":
#        G = unrelabel_G(G,slim_C_dict)
#    elif slim == "F":
#        G = unrelabel_G(G,slim_F_dict)
#    dict_file = path+"results/real_"+CID+".txt"
#    png_path = path+"results/slim_"+slim+"/real_"+CID+"/"
#    #os.system("mkdir "+png_path)
#    draw_dicts(G,dict_file,png_path)

