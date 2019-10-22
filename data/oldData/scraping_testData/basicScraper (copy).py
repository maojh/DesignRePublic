

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


content = []
headers = []
values = []
firstPub = ""

with open("pubLink_clean.csv","rb") as f:
	reader = csv.reader(f)
	next(reader, None)
	for pub in reader:
		firstPub = pub
		r = requests.get( pub[0]+'?mode=full' )
		print r.status_code
		html = "".join(line.strip() for line in r.content.split("\n"))
		soup = BeautifulSoup(html,'lxml')
		rows = soup.find_all('tr')
		for i in range(1, len(rows)-3):
			cells = rows[i].find_all('td')
			field = cells[0].string
			value  = cells[1].string
			if(field in ['dc.type.full','dc.description.full.text','dc.identifier.uri','dc.date.issued','dc.type.referee','dc.type.circulation','dc.publisher.name','dc.publisher.country','dc.publisher.place','dc.relation.ispartofbook','item.journal.title','dc.relation.medium','dc.relation.conferenceplace','dc.relation.conferencename','dc.title','dc.subject.keyowrdsita','dc.subject.keywords','item.collection','item.openaireRights','dc.description.numberofauthors','item.firstauthor']):
				headers.append(field)
				content.append(value)
			elif(field in ['dc.language.iso','dc.authority.people','item.singlekeyword','item.externalauthor','item.externalcontributor','crisitem.author.appartenenza']): #multiple value fields
				headers.append(field)
				content.append(value)
				#split keywords and allpeople, and list multiple column values
#				print field + ": " + value
#			else:
				#print "valid field? " + field
#			print field.string + ": " + value.string
		break

print headers
print content

if(len(headers)==len(content)):
	print "ok"
else:
	print "Headers fields: " + str(len(headers)) + " - Values: " + str(len(content))

time  = datetime.now()

fileName = "singolo_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

ofile = open(fileName,"wb")

writer = csv.writer(ofile,delimiter=",")
writer.writerow(headers)
writer.writerow(content)

ofile.close()

#rfile = open(fileName,"rb")

#reader = csv.reader(rfile)
#for row in reader:
#	print row

