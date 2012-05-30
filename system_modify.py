f = open("results/system_data")
g = open("results/system_data_new","w")
for line in f:
    elements = line.split("\t")
    if len(elements) == 10:
        elements[1] = int(elements[1])-1
        elements[4] = int(elements[4])-1
    for element in elements:
        g.write(str(element).strip()+"\t")
    g.write("\n")

