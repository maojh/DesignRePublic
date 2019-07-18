import csv
import sys

#print 'NU'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')

files = sys.argv[1:]
print str(files[0])

lines = []

for f in files:
    print str(f)

    ofile = open(f,"rb")
    reader = csv.reader(ofile)

    file_name = "strip_" + str(f)
    nfile = open(file_name,"wb")
    writer = csv.writer(nfile,delimiter=",")

    for row in reader:
        lines.append(["".join(row)])

    writer.writerows(lines)

    ofile.close()
    nfile.close()
