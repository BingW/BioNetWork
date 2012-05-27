import sqlite3
Coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
C = Coon.cursor()
CID2Condition = {}
for row in C.execute("SELECT * FROM CID2Condition"):
    CID2Condition[row[0]] = row[1]

reviewed = {}
#reviewed["amino_acid_st"] = ["amino acid starvation","histidine-limited"]
#reviewed["glu_limited"] = ["glucose-limited","glucose limited","low glucose"]
#reviewed["glu_normal"] = ["2% glucose","2%glucose"]
#reviewed["chem_DTT"] = ["DTT"]
#reviewed["chem_Clotrimazole"] = ["Clotrimazole"]
#reveiwed["chem_NaCl"] = ["NaCl"]
#reviewed["temp"] = ["glucose pulse","glucose depletion"]

Waiting_list = ["galactose","ethanol","EtOH","glycerol"]
condition =  "amino acid starvation"

for CID in CID2Condition:
    string = CID2Condition[CID]
    if string.count(condition) == 1:
        flag = 0
        for Class in reviewed:
            for exception in reviewed[Class]:
                if string.count(exception) == 1:
                    flag = 1
                    break
        if flag == 0:
            print string
