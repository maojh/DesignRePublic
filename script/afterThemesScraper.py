
import requests, re
from bs4 import BeautifulSoup
import csv
import sys
import glob, os
from datetime import datetime, date, timedelta

printing = True

records = []
headersPub = []
kw = []
titles = []
pubbs = []
strangeRecords = []
failedRequests = []

def openCsv(file,delimiter=','):
	a = []
	# with open(file,'r',encoding='utf-8') as f:
	with open(file,'r') as f:
		reader = csv.reader(f,delimiter=delimiter)
		h = next(reader)

		for row in f:
			curr = row.replace('\n','')
			curr = curr.split(delimiter)
			a.append(curr)
	return a, h

authors = openCsv('kwAuthor_26_10_22_52.csv','\t')
headersAuthors = authors[1]
authors = authors[0]
records = [[],[]]
 # [['names'],['keywords']]
res = [[],[]]

def getKw(index):
	i = -1
	# Get first name if more than one is found
	namess = authors[index][4].split(' ')
	name = namess[0]
	if(len(namess)>1):
		name = name + ' ' + namess[1]
	try:
		ir = records[0].index(name[0])
		aa = []
		for a in authors:
			aa.append(a[4])
		ia = aa.index(name)

		for k in authors[ia][7].split(';'):
			records[1][ir].append(k)
		records[1][ir] = list(set(records[1][ir]))
		# # i = records[0].index(authors[index][4])
		# # print(records[0][i], 'again')
		# for k in authors[index][7].split(';'):
		# 	records[1][i].append(k)
		# records[1][i] = list(set(records[1][i]))
	except:
		kws = authors[index][7].split(';')
		records[0].append(name)
		records[1].append(kws)

for i in range( 1, len(authors)):
	getKw(i)


# print(records[0][0], records[1][0])

# record = [author, kw1, kw2, kw3]
# records = [record1, record2]

time  = datetime.now()
fileName = "kwAuthor_collect_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

if(printing):
	ofile = open(fileName,"w")
	writer = csv.writer(ofile,delimiter=",")
	i = 0
	print("writing")
	writer.writerow(["name","section","ssid","keywords"])
	for i in range(len(records[0])):
		# print (str(records[:][i]))
		# break

		try:
			print(i)
			row = [records[0][i]]
			# print(authors[i][5])
			row.append(authors[i][5])
			row.append(authors[i][6])
			for k in records[1][i]:
				if not(k==''):
					row.append(k)
			writer.writerow(row)
			# break
			# print("written")
		except:
			print("failed")
			print(str(records[0][i]))
			continue

	print("Lines written " + str(i) + " of " + str(len(records[0])))
	ofile.close()
