#coding: utf-8
import sqlite3

Coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
C = Coon.cursor()
#C.execute("CREATE TABLE other2ID (other unique, SGDID)")
#C.execute("CREATE TABLE ID2Interact (SGDID_1, SGDID_2, InterType, ExpType, Phenotype)")
#C.execute("CREATE TABLE ID2Feature (SGDID, feature, stardand, Type, Descrip)")
#C.execute("CREATE TABLE ID2Product (SGDID, product)")
#C.execute("CREATE TABLE ID2Phenotype (SGDID, mutan_type, phenotype, chemical, condition, details, reporter)")
#C.execute("CREATE TABLE ID2GO (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition)")

def other2ID_init(): 
    f = open("/Users/bingwang/VimWork/db/SGD_features.tab")
    for line in f:
        elements = line.split("\t")
        C.execute("INSERT INTO ID2Feature VALUES (?,?,?,?,?)",\
                (elements[0],elements[3],elements[4],elements[1],elements[15].strip()))
        try:
            C.execute("INSERT INTO other2ID VALUES (?,?)",(elements[0],elements[0]))
        except:
            pass
        try:
            C.execute("INSERT INTO other2ID VALUES (?,?)",(elements[3],elements[0]))
        except:
            pass
        try:
            C.execute("INSERT INTO other2ID VALUES (?,?)",(elements[4],elements[0]))
        except:
            pass
        for name in elements[5].split("|"):
            try:
                C.execute("INSERT INTO other2ID VALUES (?,?)",(name,elements[0]))
            except:
                pass
        for name in elements[8].split("|"):
            try:
                C.execute("INSERT INTO other2ID VALUES (?,?)",(name,elements[0]))
            except:
                pass
    C.execute("DELETE FROM other2ID WHERE other = ''")
    #Coon.commit()

def ID2Interact_init():
    f = open("/Users/bingwang/VimWork/db/interaction_data.tab")
    for line in f:
        elements = line.split("\t")
        intertype = "G" if elements[5] == "genetic interactions" else "P"
        SGDID_1 = other2ID[elements[0]]
        SGDID_2 = other2ID[elements[2]]
        C.execute('INSERT INTO ID2Interact VALUES (?,?,?,?,?)',\
                (SGDID_1,SGDID_2,intertype,elements[4],elements[9]))
    #Coon.commit()

def ID2GO_Product_init():
    f = open("/Users/bingwang/VimWork/db/go_slim_mapping.tab")
    slim_GO = [] 
    for line in f:
        if line[0] != "!":
            elements = line.split("\t")
            try:
                goid = elements[5]
            except:
                continue
            if goid not in slim_GO:
                slim_GO.append(goid)

    f = open("/Users/bingwang/VimWork/db/go_terms.tab")
    GOID2term = {}
    for line in f:
        elements = line.split("\t")
        GOID2term["GO:"+"0"*(7-len(elements[0]))+elements[0]] = [elements[1],elements[2],elements[3].strip()]
        #GOID2term[ID] = [GO_Term,GO_Aspect,GO_Definition]
    f = open("/Users/bingwang/VimWork/db/gene_association.sgd")
    SGDID_product=[] 
    for line in f:
        if line[0] != "!":
            elements = line.split("\t")
            if elements[1] not in other2ID:
                print elements[1], "doesn't exist"
            else:
                SGDID = other2ID[elements[1]]
                GOID = elements[4]
                slim = 0 if GOID not in slim_GO else 1
                GO_Term = GOID2term[GOID][0]
                GO_Aspect = GOID2term[GOID][1]
                GO_Definition = GOID2term[GOID][2]
                C.execute("INSERT INTO ID2GO VALUES (?,?,?,?,?,?)",\
                        (SGDID,GOID,slim,GO_Term,GO_Aspect,GO_Definition))
                if elements[9] in SGDID_product:
                    continue
                else:
                    SGDID_product.append(elements[9])
                    for product in elements[9].split("|"):
                        C.execute("INSERT INTO ID2Product VALUES (?,?)",(SGDID,product)) 
    #Coon.commit()

def ID2Phenotype_init():
    f = open("/Users/bingwang/VimWork/db/phenotype_data.tab")
    for line in f:
        elements = line.split("\t")
        try:
            SGDID = other2ID[elements[3]]
        except:
            continue
        C.execute("INSERT INTO ID2Phenotype VALUES (?,?,?,?,?,?,?)", \
               (SGDID,elements[6],elements[9],elements[10],elements[11],elements[12],elements[13]))
    #Coon.commit()
