from system import *
#################
# demand_supply #
#################
f = open(path+"/results/ScerMicro_b.tab")
SGDID_list = f.readline().split("\t")[1:-1] #because nothing after the last '\t'
Microarray = np.zeros((7387,len(SGDID_list)),dtype = np.uint8)
for i,line in enumerate(f):
    elements = line.split("\t")[:-1] #because nothing after the last '\t'
    for j,num in enumerate(elements[1:]):
        Microarray[i,j] = num
    if i%50 == 0:
        print "loding Microarray "+str(round(i*100.0/7387,2))+"%"
f.close()
print "Microarray init finish!"
min_law = 10
node_list = [node for node in LAW if \
        sum([len(LAW[node][0]),len(LAW[node][1]),len(LAW[node][2])]) >= min_law]

from collections import Counter
over_exp_nodes = {}
low_exp_nodes = {}
normal_exp_nodes = {}
for i in xrange(50):
    over_exp_nodes[i] = []
    low_exp_nodes[i] =[]
    normal_exp_nodes[i] = []
for node in node_list:
    exp = Microarray[:,SGDID_list.index(node)]
    count = Counter(exp)
    count_sum = np.sum([count[0],count[1],count[2]])
    over_exp_nodes[count[1]*50/count_sum].append(node)
    low_exp_nodes[count[2]*50/count_sum].append(node)
    normal_exp_nodes[count[0]*50/count_sum].append(node)
over_exp_rates = {}
low_exp_rates = {}
normal_exp_rates = {}

for i in xrange(50):
    over_exp_rates[i] = []
    low_exp_rates[i] =[]
    normal_exp_rates[i] = []

for i in xrange(50):
    for node in over_exp_nodes[i]:
        over_exp_rates[i].append(len(LAW[node][1])*1.0/\
                sum([len(LAW[node][1]),len(LAW[node][2]),len(LAW[node][0])]))
    for node in low_exp_nodes[i]:
        low_exp_rates[i].append(len(LAW[node][2])*1.0/\
                sum([len(LAW[node][1]),len(LAW[node][2]),len(LAW[node][0])]))
    for node in normal_exp_nodes[i]:
        normal_exp_rates[i].append(len(LAW[node][0])*1.0/\
                sum([len(LAW[node][1]),len(LAW[node][2]),len(LAW[node][0])]))
for i in xrange(10):
    print sum(over_exp_rates[i]) / len(over_exp_rates[i])

for i in xrange(10):
    print sum(low_exp_rates[i]) / len(low_exp_rates[i])
left_sum = 0
left_count = 0
for i in xrange(10,50,1):
    left_sum += sum(low_exp_rates[i]) 
    left_count += len(low_exp_rates[i])
print left_sum / left_count

for i in xrange(40,49,1):
    print sum(normal_exp_rates[i]) / len(normal_exp_rates[i])
left_sum = 0
left_count = 0
for i in xrange(0,40,1):
    left_sum += sum(normal_exp_rates[i]) 
    left_count += len(normal_exp_rates[i])
print left_sum / left_count
