import mechanize
import os
from time import sleep
br = mechanize.Browser()
br.set_handle_robots(False)  #ignore robots.txt
br.open('http://www.yeastgenome.org/download-data/expression')
folder=[]
for l in br.links(): 
    if l.url.startswith("http://downloads.yeastgenome.org/expression/microarray/"):
        folder.append(l.url)

pcl_path = []
for thing in folder:
    #cmd = "mkdir ~/VimWork/BioNetWork/Microarray/"+thing.split("/")[-2]
    #os.system(cmd)
    if thing.count("PMID") == 1:
        pcl_path.append(thing[:thing.rfind("/")])


for pcl_p in pcl_path:
    has = os.listdir("/Users/bingwang/VimWork/db/Microarray"+ \
        pcl_p[pcl_p.rfind("/"):])
    if "README" not in has:
        br.open(pcl_p+"/"+"README")
        R = open("/Users/bingwang/VimWork/db/Microarray"+ \
            pcl_p[pcl_p.rfind("/"):]+"/README","w")
        R.write(br.response().read())
        sleep(1)
    else:
        print "README exists"
    br.open(pcl_p)
    pcl_file_link = []
    for l in br.links():
        if l.url.endswith(".pcl"):
            pcl_file_link.append(l.url)
    for url in pcl_file_link:
        if url not in has:
            pcl_write = "/Users/bingwang/VimWork/db/Microarray"+\
                    pcl_p[pcl_p.rfind("/"):]+"/"+url
            print pcl_write
            P = open(pcl_write,"w")
            br.open(pcl_p+"/"+url)
            P.write(br.response().read())
            sleep(1)
        else:
            print url,"exists"


'''
br.open("http://downloads.yeastgenome.org/expression/microarray/archive/Expression_connection_data/")
pcl_file = []
for l in br.links():
    if l.url.endswith(".pcl.gz"):
        pcl_file.append(l.url)
for link in pcl_file:
    path = "http://downloads.yeastgenome.org/expression/microarray/archive/Expression_connection_data/"+link
    f = open("/Users/bingwang/VimWork/db/Microarray/archive/"+link,"w")
    br.open(path)
    f.write(br.response().read())
    print link,"finish"
    sleep(1)
'''
'''
def downloadlink(l):
    f=open(l.text,"w") #perhaps you should open in a better way & ensure that file doesn't already exist.
    br.click_link(l)
    f.write(br.response().read())
    print l.text," has been downloaded"
    #br.back()

for l in myfiles:
    sleep(1) #throttle so you dont hammer the site
    downloadlink(l)
'''
