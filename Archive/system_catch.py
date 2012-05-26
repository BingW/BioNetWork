import os
g = open("system_data","w")
for l in os.listdir("/Users/bingwang/VimWork/BioNetWork/Archive/"):
    if l.endswith(".tab"):
        f = open(l)
        g.write(f.read())

