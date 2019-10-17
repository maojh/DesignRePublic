
import requests, re
from bs4 import BeautifulSoup
import csv
import sys
import glob, os
from datetime import datetime, date, timedelta

print "starting"
reload(sys)
sys.setdefaultencoding('utf8')

stop = -1
args = sys.argv[1:];

records = []
headers = ["title","author","year","type","keywords","cluster","collection"]
strangeRecords = []
i = 0

# with open("data4temi.csv","rb") as f:
with open(args[0],"rb") as f:
	reader = csv.reader(f)
	header = next(reader, None)
	for pub in reader:
		print ("starting")

		if(stop>0 and i>stop):
			print ("stopping")
			break

		print ( "Scraping: " + pub[0] )
		content = []
		# indexes search
		type = pub[header.index("item.collection")]

		if(type.__contains__("convegno")):
				if(header.index("dc.title")>=0):
					title = str(pub[header.index("dc.title")])
				elif(header.index("dc.relation.conferencename")>=0):
					title = str(pub[header.index("dc.relation.conferencename")])
				else:
					strangeRecords.append(pub)
					title = "---"
		else:
			title = str(pub[header.index("dc.title")])

		title = title.replace("'","\'")
		content.append(title)
		content.append( pub[header.index("dc.authority.people")])
		content.append( pub[header.index("dc.date.issued")])
		content.append( str(type) )
		content.append( pub[header.index("dc.subject.keywords")])
		content.append( "nocluster" )
		print ( content )
		if(len(content)<6):
			strangeRecords.append(pub)
			print ( pub[0] + " is a strange records" )
		else:
			records.append(content)
		i += 1

#print headers
#print "All records: "
#print records
if (len(strangeRecords)>0):
	print ( "strange records are " + str(len(strangeRecords)) )

time  = datetime.now()

fileName = "titles_" + str(args[0][11:-5]) + "_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

ofile = open(fileName,"wb")

writer = csv.writer(ofile,delimiter=",")
writer.writerow(headers)
for rec in records:
	writer.writerow(rec)

ofile.close()

#rfile = open(fileName,"rb")

#reader = csv.reader(rfile)
#for row in reader:
#	print row

#rfile.close()

#sys.exit()
