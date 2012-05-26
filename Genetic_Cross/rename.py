import os
path = "/Users/bingwang/VimWork/BioNetWork/Genetic_Length/"
for fi in os.listdir(path):
    if fi.endswith(".png"):
        if len(fi) == 6:
            os.system("mv "+path+fi+" "+path+"0"+fi)
        if len(fi) == 5:
            os.system("mv "+path+fi+" "+path+"00"+fi)
