import csv

ofile = open('Temi/mergeKeywords.csv','r')
oreader = csv.reader(ofile,delimiter=',')
header = next(oreader)

sections = []
kws = []
sectionkw = [[],[]]

for row in oreader:
    sections.append(row[6])
    k = row[11].split(';')
    kws.append(k)
    sectionkw.append([row[6],k])

sections = list(set(sections))
sectionkw = sectionkw[3:]

result = [sections,[[],[],[],[],[]]]

# print(sections[3])

# print(str(sections[2]),str(sectionkw[0][0]))

for sec in sections:
    print(sec)
    ir = 'n'
    for i in range(len(sectionkw)):
        print(i)
        if(sec==sectionkw[i][0]):
            ir = result[0].index(sec)
            for k in sectionkw[i][1]:
                result[1][ir].append(k)
    result[1][ir] = list(set(result[1][ir]))

nfile = open('sectionKw.csv','w')
nwriter = csv.writer(nfile)

for j in range(len(sections)):
    row = []
    row.append(result[0][j])
    for k in result[1][j]:
        row.append(k)
    nwriter.writerow(row)
