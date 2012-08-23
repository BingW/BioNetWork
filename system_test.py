from system import *
M_coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
M_c = M_coon.cursor()
CID2Condition = {}
scores = []
for row in M_c.execute("SELECT * FROM CID2Condition"):
    CID2Condition[row[0]] = row[1]

######################
#    single test     #
######################
balance_left = 0.0
balance_right = 0.1
for CID in CID2Condition:
    dict_CID = get_input(CID)
    balance_rate = calculate_balance(dict_CID)
    if balance_left < balance_rate <= balance_right:
        print CID, balance_rate
        scores.append(predict_one(dict_CID))
    if len(scores) > 10:
        break

print scores 
print sum(scores) * 1.0 / 10
#####################
#    series_test    #
#####################
condition_series = "11102521_0"
CID_list = []
for CID in CID2Condition:
    if condition_series in CID:
        print CID,CID2Condition[CID]
        CID_list.append(CID)
CID_list.sort()
return_dict = predict_series(series_data[0],50,real_CIDs=CID_list,\
        out_file=path+"results/"+condition_series)
