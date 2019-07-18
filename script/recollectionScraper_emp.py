

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

chunk = sys.argv[1:];


for c in chunk:
	records = []
	headers = []
	headers = ['dc.identifier.uri','item.collection']
	strangeRecords = []
	emptyRows = []
	failedRequests = []
	stop = 3	#early stop for testing
	count = 0	#early stop for testing

	time  = datetime.now()

	fileName = "recollection_empties_p" + c + "-" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

	ofile = open(fileName,"wb")

	writer = csv.writer(ofile,delimiter=",")
	writer.writerow(headers)

	#update with right format name
	linkFile = "collection_empties_p" + c + "_2.csv"

	with open(linkFile,"rb") as f:
		reader = csv.reader(f)
		next(reader, None)
		for pub in reader:
#			print "Scraping: " + pub[0]
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
						cells = rows[i].find_all('th')

					if (cells == []):
						emptyRows.append(pub[0])
						print rows[i]
						print "Found empty cells?! at ", pub[0]
						break


					field = cells[0].string		#at there is still an header in cells https://re.public.polimi.it/handle/11311/1008787
					value  = cells[1].string

#					if(field in ['dc.identifier.uri','item.collection']):
					if(field in ['dc.identifier.uri','dc.type.full']):
						print value, not(value=="")
						if value=="":
							break
						content.append(value)
						records.append(content)

				writer.writerow(content)

				count = count + 1
				#Testing: stop after 3 pubs
#				if count==stop:
#					break
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

	ofile.close()

	# save error links in  a file

	fileNameE = "collection_empties_p" + c + "_" +  str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"
	fileNameF = "collection_failed_p" + c + "_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

	ofileE = open(fileNameE, "wb")
	ofileF = open(fileNameF, "wb")

	writerE = csv.writer(ofileE,delimiter=",")
	writerE.writerow(["emptyRows"])
	for linkE in emptyRows:
		writerE.writerow([linkE])

	writerF = csv.writer(ofileF,delimiter=",")
	writerF.writerow(["failedRequests"])
	for linkF in failedRequests:
		writerF.writerow([linkF])

	ofileE.close()
	ofileF.close()


#sys.exit()
