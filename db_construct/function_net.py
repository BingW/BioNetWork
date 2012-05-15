#coding: utf-8
f = open("/Users/bingwang/VimWork/db/SGD_features.tab")
other2ID = {}
#other2ID[other] = ID
ID2Feature = {}
#ID2Feature[ID] = [feature_name,stardand_name,Type,Description]
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
        ID2Feature[elements[0]] = [elements[3],elements[4],elements[1],elements[15].strip()]
        other2ID[elements[0]] = elements[0]
        other2ID[elements[3]] = elements[0]
        other2ID[elements[4]] = elements[0]
        for name in elements[5].split("\t"):
            other2ID[name] = elements[0]
        for name in elements[8].split("\t"):
            other2ID[name] = elements[0]

f = open("/Users/bingwang/VimWork/db/interaction_data.tab")
ID2Interact = {}
#ID2Interact[ID_B][ID_H] = [["Bait_Hit","Genetic",ExpType,Phenotype],...]
for line in f:
    elements = line.split("\t")
    inter_type = "G" if elements[5] == "genetic interactions" else "P"
    if elements[0] in other2ID and elements[2] in other2ID:
        ID_B = other2ID[elements[0]]
        ID_H = other2ID[elements[2]]
    else:
        print elements[0], "or", elements[1],"doesn't exist"
    if ID_B not in ID2Interact:
        ID2Interact[ID_B] = {}
    if ID_H not in ID2Interact[ID_B]:
        ID2Interact[ID_B][ID_H] = []
    ID2Interact[ID_B][ID_H].append(["Bait_Hit",inter_type,elements[4],elements[9]])
    if ID_H not in ID2Interact:
        ID2Interact[ID_H] = {}
    if ID_B not in ID2Interact[ID_H]:
        ID2Interact[ID_H][ID_B] = []
    ID2Interact[ID_H][ID_B].append(["Hit_Bait",inter_type,elements[4],elements[9]])

f = open("/Users/bingwang/VimWork/db/go_slim_mapping.tab")
ID2slim_GO = {}
#ID2slim_GO[ID] = [GOID1,GOID2...]
for line in f:
    if line[0] != "!":
        elements = line.split("\t")
        if elements[2] not in other2ID:
            print elements[2], "doesn't exist"
        else:
            if elements[5]!= "":
                if elements[2] in ID2slim_GO:
                    ID2slim_GO[elements[2]].append(str(int(elements[5].split(":")[1])))
                else:
                    ID2slim_GO[elements[2]] = [str(int(elements[5].split(":")[1]))]
             
f = open("/Users/bingwang/VimWork/db/gene_association.sgd")
ID2GO = {}
#ID2GO[ID] = [GOID1,GOID2...]
ID2Product = {}
#ID2Product[ID] = [Product1,Product2...]
for line in f:
    if line[0] != "!":
        elements = line.split("\t")
        if elements[1] not in other2ID:
            print elements[1], "doesn't exist"
        else:
            if elements[1] in ID2GO:
                ID2GO[elements[1]].append(str(int(elements[4].split(":")[1])))
                for name in elements[9].split("|"):
                    if name not in ID2Product[elements[1]]:
                        ID2Product[elements[1]].append(elements[9])
            else:
                ID2GO[elements[1]] = [str(int(elements[4].split(":")[1]))]
                ID2Product[elements[1]] = []
                for name in elements[9].split("|"):
                    if name not in ID2Product[elements[1]]:
                        ID2Product[elements[1]].append(name)

f = open("/Users/bingwang/VimWork/db/go_terms.tab")
GO_ID2term = {}
#GO_ID2term[ID] = [GO_Term,GO_Aspect,GO_Definition]
for line in f:
    elements = line.split("\t")
    GO_ID2term[elements[0]] = [elements[1],elements[2],elements[3].strip()]

f = open("/Users/bingwang/VimWork/db/phenotype_data.tab")
ID2Pheno = {}
#ID2Pheno[ID] = [[mutan_type,phenotype,chemical,condition,details,reporter],...]
for line in f:
    elements = line.split("\t")
    if elements[3] not in other2ID:
        #print elements[3], "merged or deleted"
        pass
    else:
        if elements[3] in ID2Pheno:
            ID2Pheno[elements[3]].append([elements[6],elements[9],elements[10],\
                    elements[11],elements[12],elements[13]])
        else:
            ID2Pheno[elements[3]] = [[elements[6],elements[9],elements[10],\
                    elements[11],elements[12],elements[13]]]

H_Type = []

f = open("/Users/bingwang/VimWork/BioNetWork/function.txt","w")
for ID in ID2Feature:
#ID2Feature[ID] = [feature_name,stardand_name,Type,Description]
    #other2ID[other] = ID
#ID2Product[ID] = [Product1,Product2...]
#ID2GO[ID] = [GOID1,GOID2...]
    #GO_ID2term[ID] = [GO_Term,GO_Aspect,GO_Definition]
#ID2Pheno[ID] = [[mutan_type,phenotype,chemical,condition,details,reporter],...]
#ID2Interact[ID_B][ID_H] = [["Bait_Hit","Genetic",ExpType,Phenotype],...]
    name = ID2Feature[ID][1] if ID2Feature[ID][1] != "" else ID2Feature[ID][0]
    #condition = True 
    condition = (name != "")# and ID2Feature[ID][2] == "not physically mapped")
    #standard_name if has standard_name else system_name
    if condition:
        f.write(name+":\t\n")
        if ID2Feature[ID][2] not in H_Type:
            H_Type.append(ID2Feature[ID][2])
        f.write("\t#Type\t"+ID2Feature[ID][2]+"\n")
        #if name == "" and ID2Feature[ID][3] != "":
        #    print ID2Feature[ID][3]
        f.write("\t#Description\t"+ID2Feature[ID][3]+"\n")
        if ID in ID2Product:
            #if name == "":
            #    print ID2Product[ID]
            for product in ID2Product[ID]:
                f.write("\t#Product\t"+product+"\n")
        if ID in ID2slim_GO:
            for GO_ID in sorted(ID2slim_GO[ID]):
                #if GO_ID2term[GO_ID][1] not in H_Type:
                    #H_Type.append(GO_ID2term[GO_ID][1])
                f.write("\t#GO:\t"+GO_ID2term[GO_ID][1]+"\t"+GO_ID2term[GO_ID][0]+"\t\n")
        if ID in ID2Pheno:
            for pheno in sorted(ID2Pheno[ID]):
               # if pheno[0] not in H_Type:
                   # H_Type.append(pheno[0])
                f.write("\t#Phenotype:\t"+pheno[0]+"\t"+pheno[1]+"\t"+pheno[2]+"\n") 
        if ID in ID2Interact:
            #if name == "":
            #    print ID
            for ID_B in ID2Interact[ID]:
                name_B = ID2Feature[ID_B][1] if ID2Feature[ID_B][1] != "" else ID2Feature[ID_B][0]
                for inter in sorted(ID2Interact[ID][ID_B]):
                  #  if inter[0] not in H_Type:
                   #     H_Type.append(inter[0])
                    f.write("\t#Interaction\t"+name_B+"\t"+inter[0]+"\t"+\
                            inter[1]+"\t"+inter[2]+"\t"+inter[3]+"\n")
print H_Type

