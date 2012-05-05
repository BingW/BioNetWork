#coding: utf-8
import os
import numpy
import math

def float_dict(_dict):
    _out = []
    for _num in _dict:
        try:
            _out.append(float(_num))
        except:
            _out.append(float("nan"))
    return _out

def log_transmit(in_dict):
    _avg = numpy.mean([_x for _x in in_dict if math.isnan(_x) == False])
    return [math.log((_x/_avg),2) for _x in in_dict]

def is_log_transmit(in_dict):
    _valid = [_x for _x in in_dict if math.isnan(_x) == False]
    if len(_valid) == 0:
        return None
    else:
        return True if min(_valid) < 0 else False

def check_file_log_status(filename):
    _f = open(filename)
    _f.readline()
    _f.readline()
    _flag = False
    for _i in range(20):
        _m_array = _f.readline().replace("\n","").replace("\r","").split("\t")[3:]
        if is_log_transmit(float_dict(_m_array)) == True:
            _flag = True
    return _flag

def log_file(in_file,out_file=None):
    if out_file == None:
        out_file = in_file+".log"
    _f = open(in_file)
    _g = open(out_file,"w")
    _g.write(f.readline())
    _g.write(f.readline())
    for _line in _f:
        _m_array = _line.replace("\n","").replace("\r","").split("\t")
        for _item in _m_array[:3]:
            _g.write(_item+"\t")
        _m_array = log_transmit(float_dict(_m_array[3:]))
        for _num in _m_array[:-1]:
            _g.write(str(_num)+"\t")
        _g.write(str(_m_array[-1])+"\n")
    return True

def save_dict(dict_0,out_file):
    _f = open(out_file,"w")
    for _item in dict_0:
        _f.write(">"+_item+"\n")
        _f.write(dict_0[_item])

if __name__ == "__main__":
    Microarray_Path = "/Users/bingwang/VimWork/db/Microarray/"
    PMID2Readme = {} 
    for data_set in os.listdir(Microarray_Path):
        if data_set.count("PMID") == 0:
            continue
        PMID = data_set.split("_")[-1]
        f = open(Microarray_Path+data_set+"/README")
        PMID2Readme[PMID] = f.read()

        pclfiles = [pcl for pcl in os.listdir(Microarray_Path+data_set) if pcl.endswith(".pcl")]
        for i,pclfile in enumerate(pclfiles):
            if check_file_log_status(Microarray_Path+data_set+"/"+pclfile):
                try:
                    open(Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl")
                    print "existed\t"+Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl"
                except:
                    os.system("cp "+Microarray_Path+data_set+"/"+pclfile+" "+\
                            Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl")
            else:
                try:
                    open(Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl")
                    print "existed\t"+Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl"
                except:
                    in_file = Microarray_Path+data_set+"/"+pclfile
                    out_file = Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl"
                    if log_file(in_file,out_file):
                        print "add\t"+Microarray_Path+"archive/"+PMID+"_"+str(i)+".pcl"
    save_dict(PMID2Readme,Microarray_Path+"archive/"+"README")
