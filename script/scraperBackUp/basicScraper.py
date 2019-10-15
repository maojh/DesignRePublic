
import requests, re
from bs4 import BeautifulSoup
import csv
import sys
import glob, os
from datetime import datetime, date, timedelta

print "starting"
reload(sys)
sys.setdefaultencoding('utf8')

#r = requests.get("https://re.public.polimi.it/handle/11311/1019072?mode=full")
#if r is not None:
#	print "request gone wrong"
#html = "".join(line.strip() for line in r.content.split("\n"))
#soup = BeautifulSoup(html, 'lxml')

#rows = soup.find_all('tr')


records = []
headers = []
strangeRecords = []
failedRequests = []

with open("pubLink_clean.csv","rb") as f:
	reader = csv.reader(f)
	next(reader, None)
	for pub in reader:
		print "Scraping: " + pub[0]
		try:
			# r = requests.get( pub[0]+'?mode=full' )
			r = requests.get( pub[0]+'?mode=full' )
			r.raise_for_status()
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			failedRequests.append(pub[0])
			print e


		print r.status_code

		html = "".join(line.strip() for line in r.content.split("\n"))
		soup = BeautifulSoup(html,'lxml')
		rows = soup.find_all('tr')

		try:
			content = []

			for i in range(1, len(rows)-3):
				cells = rows[i].find_all('td')
				if (cells ==  []):
					break

				field = cells[0].string		#at there is still an header in cells https://re.public.polimi.it/handle/11311/1008787
				value  = cells[1].string

				if(field in ['dc.type.full','dc.description.full.text','dc.identifier.uri','dc.date.issued','dc.type.referee','dc.type.circulation','dc.publisher.name','dc.publisher.country','dc.publisher.place','dc.relation.ispartofbook','item.journal.title','dc.relation.medium','dc.relation.conferenceplace','dc.relation.conferencename','dc.title','dc.subject.keyowrdsita','dc.subject.keywords','item.collection','item.openaireRights','dc.description.numberofauthors','item.firstauthor']):
					headers.append(field)
					content.append(value)
					if(field == "dc.title"): print value

				elif(field in ['dc.language.iso','dc.authority.people','item.singlekeyword','item.externalauthor','item.externalcontributor','crisitem.author.appartenenza']): #multiple value fields
					headers.append(field)
					content.append(value)
					#split keywords and allpeople, and list multiple column values
#					print field + ": " + value
#				else:
					#print "valid field? " + field
#					print field.string + ": " + value.string	#print all available fields

				records.append(content)
#			if (pub[0] == "https://re.public.polimi.it/handle/11311/999915"):
			#Testing: stop after 3 pubs
		except:
			strangeRecords.append(pub)
			print pub[0] + " is a strange records"


#print headers
#print "All records: "
#print records
print "strange records are " + str(len(strangeRecords))
print "failed", str(len(failedRequests)), " requests"

if(len(headers)==len(content)):
	print "ok"
else:
	print "Headers fields: " + str(len(headers)) + " - Values: " + str(len(content))

time  = datetime.now()

fileName = "singolo_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

ofile = open(fileName,"wb")

writer = csv.writer(ofile,delimiter=",")
writer.writerow(headers)
for rec in records:
#	print rec
	writer.writerow(rec)

ofile.close()

#rfile = open(fileName,"rb")

#reader = csv.reader(rfile)
#for row in reader:
#	print row

#rfile.close()

#sys.exit()
