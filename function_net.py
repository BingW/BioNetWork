f = open("/Users/bingwang/VimWork/db/SGD_features.tab")
feature = {}
name2ID = {}
ID2name = {}
for line in f:
    elements = line.split("\t")
    try:
        ID2name[elements[0]]
        feature[elements[0]]
        print "ERROR",line
    except:
        ID2name[elements[0]] = []
        feature[elements[0]] = {}
        feature[elements[0]]["description"] = elements[15].strip()
        feature[elements[0]]["genetic_pos"] = elements[12]


'''
f = open("/Users/bingwang/VimWork/db/gene_association.sgd")
for line in f:
    elements = line.split("\t")
    try:
        feature[elements[1]]["product"]
    except:
        feature[elements[1]] = {}
        feature[elements[1]]["product"] = elements[9]

f = open("/Users/bingwang/VimWork/db/phenotype_data.tab")
for line in f:
    elements = line.split("\t")
    try:
        feature[elements[4]]["P"]["mutant_type"].append(elements[6])
        feature[elements[4]]["P"]["phenotype"].append(elements[9])
        feature[elements[4]]["P"]["chemical"].append(elements[10])
        feature[elements[4]]["P"]["condition"].append(elements[11])
        feature[elements[4]]["P"]["details"].append(elements[12])
        feature[elements[4]]["P"]["reporter"].append(elements[13])
    except:
        feature[elements[4]]["P"] = {}
        feature[elements[4]]["P"]["mutant_type"]=[elements[6]]
        feature[elements[4]]["P"]["phenotype"]=[elements[9]]
        feature[elements[4]]["P"]["chemical"]=[elements[10]]
        feature[elements[4]]["P"]["condition"]=[elements[11]]
        feature[elements[4]]["P"]["details"]=[elements[12]]
        feature[elements[4]]["P"]["reporter"]=[elements[13]]

f = open("/Users/bingwang/VimWork/db/interaction_data.tab")

f = open("/Users/bingwang/VimWork/db/Pillars.tab")
'''


#f = open("/Users/bingwang/VimWork/function.bingnote","w")
#for name in feature:
#    condition = feature[name] != ""
#    if condition:
#        f.write(name+"\t"+feature[name])
#        print "#"*(len(name)+8)
#        print "#  ",name,"  #"
#        print "#"*(len(name)+8)
#        print feature[name]
#        i += 1 
#    if i == once:
#        break
