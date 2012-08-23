import numpy as np
def load_dicts(dict_file):
    f = open(dict_file)
    line_1 = f.readline().split("\t")[:-1]
    input_dicts = []
    for line in f:
        input_dict = {}
        for i,value in enumerate(line.split("\t")[:-1]):
            input_dict[line_1[i]] = int(value)
        input_dicts.append(input_dict)
    return input_dicts

def calculate_balance(status_dict):
    status = np.zeros([3])
    _99 = 0
    for node in status_dict:
        if status_dict[node] == 99:
            _99 += 1
        else:
            status[status_dict[node]] += 1
    status = status / len(status_dict)
    _99 = _99 / len(status_dict)
    return status

CID = "11102521_3"
path = "/Users/bingwang/VimWork/BioNetWork/results/"
real_dicts = load_dicts(path+CID+".real")
pre_dicts = load_dicts(path+CID+".predict")
print "real_dict"
print "\'low exp\t\'over exp\t"
for real_dict in real_dicts:
    status = calculate_balance(real_dict)
    print round(status[2],4),"\t",round(status[1],4)
'''
print "predict_dict"
for pre_dict in pre_dicts:
    status = calculate_balance(pre_dict)
    print "2\t",round(status[2],4),"\t1\t",round(status[1],4)
print "Done"
'''


