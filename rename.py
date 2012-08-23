path = "/Users/bingwang/VimWork/BioNetWork/results/"
import os
path_add = "slim_F/real_11102521_15/2/"
path += path_add
for name in os.listdir(path):
    if name.endswith(".png"):
        if len(name) == 5:
            name_new = "00"+name
            cmd = "mv "+path+name+" "+path+name_new
            os.system(cmd)
        elif len(name) == 6:
            name_new = "0"+name
            cmd = "mv "+path+name+" "+path+name_new
            os.system(cmd)
        else:
            print name
