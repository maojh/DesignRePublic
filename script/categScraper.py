
import requests, re
from bs4 import BeautifulSoup
import csv
import sys
import glob, os
from datetime import datetime, date, timedelta

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print "starting"
reload(sys)
sys.setdefaultencoding('utf8')

testing = False

catName = sys.argv[1:];

records = []
headers = []

strangeRecords = []
emptyRows = []
failedRequests = []

time  = datetime.now()

fileName = "../data/" + str(catName[0]) + "3_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"
ofile = open(fileName,"wb")
writer = csv.writer(ofile,delimiter=",")
linkFile = "../data/data3" + str(catName[0]) + ".csv"
counter = 0

with open(linkFile,"rb") as f:
	reader = csv.reader(f)
	next(reader, None)
	for pub in reader:
		pub[1] = "https://re.public.polimi.it/handle/11311/" + pub[1][28:] + "?mode=full"
		print "Scraping: " + pub[1] + " " + pub[0]
		counter = counter + 1
		# print pub[1]
		try:
			r = requests.get( pub[1] )
			print bcolors.OKBLUE + str(r.status_code) + bcolors.ENDC
			r.raise_for_status()
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			failedRequests.append(pub[1])
			print e


		html = "".join(line.strip() for line in r.content.split("\n"))
		soup = BeautifulSoup(html,'lxml')
		rows = soup.find_all('tr')

		try:
		 	# content = ['-'] * len(rows)
			content = []
#
			headers = []
#
			lastField = ""
			for i in range(1, len(rows)-3):
				cells = rows[i].find_all('td')
				if (cells ==  []):
					cells = rows[i].find_all('th')
					if (cells == []):
						emptyRows.append(pub[0])
						print "Found empty row?! at ", pub[1]
						break

				field = cells[0].string		#at there is still an header in cells https://re.public.polimi.it/handle/11311/1008787
				value  = cells[1].string

				# content = ['-'] * len(rows)

				if(field in ['dc.type.full','dc.description.full.text','dc.identifier.uri','dc.date.issued','dc.type.referee','dc.type.circulation','dc.publisher.name','dc.publisher.country','dc.publisher.place','dc.relation.ispartofbook','item.journal.title','dc.relation.medium','dc.relation.conferenceplace','dc.relation.conferencename','dc.title','dc.subject.keyowrdsita','dc.subject.keywords','item.collection','item.openaireRights','dc.description.numberofauthors']):
					if(field in headers):
						print ""
					# 	pos = headers.index(field)
					# 	content[pos] = value
					else:
						headers.append(field)
						content.append(value)
					# 	headers.append(field)
					# 	content.append(value)

					# content.append(value)
					# headers.append(field)
				elif(field in ['dc.language.iso','dc.authority.people']): #multiple value fields
						# ,'item.externalauthor','item.externalcontributor'
					print 'elif'
					# headers.append(field)
					# content.append(value)

					if(field in headers):
						print ""
					# 	pos = headers.index(field)
					# 	if(field==lastField):
					# 		content[-1] += ";" + value
						# else:
					# 		content[pos] = value
					else:
						headers.append(field)
						if(field==lastField):
							content[-1] += ";" + value
						else:
							content.append(value)
					# if(field==lastField):
					# 	content[-1] += ";" + value
					# else:
					# 	content.append(value)
				# print " ".join(content)

				lastField = field

			records.append(headers)
			records.append(content)

			#Testing: stop after 3 pubs
		except Exception as e:
			print bcolors.WARNING + str(e) + bcolors.ENDC
			strangeRecords.append(pub)
			print pub[1] + " is a strange records"


		print 'counter ' + str(counter)
		print ""
		if (testing == True and counter == 10):
			break
		break

writer.writerow( headers )
writer.writerows( records )

#print headers
#print "All records: "
#print records
print "strange records are " + str(len(strangeRecords))
print "failed", str(len(failedRequests)), " requests"
print "---"
print "written ", str(len(records)), " records"

ofile.close()

# save error links in  a file

#fileNameE = str(catName[0]) + "3_empties_" +  str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"
#fileNameF = str(catName[0]) + "3_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"


#ofileE = open(fileNameE, "wb")
#ofileF = open(fileNameF, "wb")

#writerE = csv.writer(ofileE,delimiter=",")
#writerE.writerow(["emptyRows"])
#for linkE in emptyRows:
#	writerE.writerow(linkE)

#writerF = csv.writer(ofileF,delimiter=",")
#writerF.writerow(["failedRequests"])
#for linkF in failedRequests:
#	writerF.writerow(linkF)

#ofileE.close()
#ofileF.close()

#sys.exit()
