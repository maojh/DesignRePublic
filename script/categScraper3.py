
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

print ("starting")
# reload(sys)
# sys.setdefaultencoding('utf8')

testing = False

catName = sys.argv[1:];

records = []
headers = []

strangeRecords = []
emptyRows = []
failedRequests = []

time  = datetime.now()

fileName = "../data/" + str(catName[0]) + "5_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"
ofile = open(fileName,"w",encoding='utf8')
writer = csv.writer(ofile,delimiter=",")
linkFile = "../data/pubLink_part/data3" + str(catName[0]) + ".csv"
# linkFile = "../data/data3" + str(catName[0]) + ".csv"
counter = 0

with open(linkFile,"r") as f:
    reader = csv.reader(f)
    next(reader, None)
    for pub in reader:
        pub[1] = "https://re.public.polimi.it/handle/11311/" + pub[1][28:] + "?mode=full"
        print( "Scraping: " + pub[1] )
        print( pub[0] )
        counter = counter + 1
        # print pub[1]
        try:
            r = requests.get( pub[1] )
            print (bcolors.OKBLUE + str(r.status_code) + bcolors.ENDC)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            failedRequests.append(pub[1])
        test = type
        html = "".join(line.strip() for line in r.content.decode().split("\n"))
        soup = BeautifulSoup(html,'lxml')
        rows = soup.find_all('tr')

        try:
             # content = ['-'] * len(rows)
            content = []
            headers = []

            lastField = ""
            for i in range(1, len(rows)-3):
                cells = rows[i].find_all('td')
                if (cells ==  []):
                    cells = rows[i].find_all('th')
                    if (cells == []):
                        emptyRows.append(pub[0])
                        print ( "Found empty row?! at ", pub[1] )
                        break

                field = cells[0].string        #at there is still an header in cells https://re.public.polimi.it/handle/11311/1008787
                value  = cells[1].string

                # content = ['-'] * len(rows)

                if(field in ['dc.type.full','dc.description.full.text','dc.identifier.uri','dc.date.issued','dc.type.referee','dc.type.circulation','dc.description.allpeople','dc.publisher.name','dc.publisher.country','dc.publisher.place','dc.relation.ispartofbook','item.journal.title','dc.relation.medium','dc.relation.conferenceplace','dc.relation.conferencename','dc.title','dc.subject.keywordsita','dc.subject.keywords','item.collection','item.openaireRights','dc.description.numberofauthors']):
                    headers.append(field)
                    content.append(value)
                # elif(field in ['dc.language.iso','dc.authority.people']): #multiple value fields
                elif(field in ['dc.language.iso']): #multiple value fields
                    if(field==lastField):
                        content[-1] += ";" + value
                        print("multiple field " + field + ": " + value)
                    else:
                        headers.append(field)
                        content.append(value)
                lastField = field

            # for h in range(len(headers)):
            #     print str(headers[h]) + ' ' + str(content[h])
            print( str(counter) )
            records.append([headers,content])
            print ("")
            #Testing: stop after 3 pubs
        except Exception as e:
            print ( bcolors.WARNING + str(e) + bcolors.ENDC )
            strangeRecords.append(pub)
            print ( pub[1] + " is a strange records" )
        # break

allHeaders = []

for r in records:
    for h in r[0]:
        allHeaders.append(h)

print ( "records number: " )
print ( len(records) )
print ( "" )

setHeaders = set(allHeaders)
headers = list(setHeaders)
# print str(headers) + " | " + str(len(headers))

print ("writing")
writer.writerow(headers)

count = 0

for record in records:
    content = ['-'] * len(headers)
    for head in headers:
        if(head in record[0]):
            pos = record[0].index(head) #-1
            posH = headers.index(head)
            try:
                #content.append(record[1][pos])
                content[posH] = record[1][pos]
            except Exception as e:
                counter += 1
#                print "field: " + str(record[0][pos]) + " " + str(pos)
#                print "value: " + str(record[1]) + " " + str(pos)
                print ( 'pos ' + str(pos) + 'at' + str(len(headers)) +' / ' + str(len(record[1])) )
                print ( e )
                print ("")
                content.append("XXXXXXXXXXXXXXXXXXXX")
        else:
            posH = headers.index(head)
            content[posH] = '-'
#            content.append("-")

    writer.writerow(content)
    # break
print ("")

print ("")
print ("strange records are " + str(len(strangeRecords)))
print ("failed", str(len(failedRequests)), " requests")
print ("---")
print ("written ", str(len(records)), " records")

ofile.close()

def lookRecord(i):
    for n in range(0,len(records[i][1])):
        print( records[i][0][n] + ": " + records[i][1][n])
