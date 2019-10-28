
import requests, re
from bs4 import BeautifulSoup
import csv
import sys
import glob, os
from datetime import datetime, date, timedelta

records = []
headersPub = []
kw = []
titles = []
pubbs = []
strangeRecords = []
failedRequests = []

def openCsv(file,delimiter=','):
	a = []
	with open(file,'r',encoding='utf-8') as f:
		reader = csv.reader(f,delimiter=delimiter)
		h = next(reader)

		for row in f:
			curr = row.replace('\n','')
			curr = curr.split(delimiter)
			a.append(curr)
	return a, h


pubbs = openCsv('data5d.csv','\t')
headersPub = pubbs[1]
pubbs = pubbs[0]
kw = openCsv('kw4.csv')
headersKw = kw[1]
kw = kw[0]

authors = openCsv('Temi/network_ext_edges.csv')
headersAuthors = authors[1]
authors = authors[0]
# search for keywords in articles, kes has been found in the titles dataset already
stop = -1
i = 0
notValid = []
empties = []
kfound = []
namesFound = 0
records = []

for p in pubbs:
	if p==['']:
		print("empty pubb? " + str(i))
		continue
	newpub = []
	section = '-'
	ssid = '-'
	aname = ''
	pubAuthors = ""
	# if(len(p)<4):
	# 	# break
	# 	p = p[0].split(',')
	# 	if(len(p)<4):
	# 		notValid.append(p)
	# 		print("not valid" + ' ' + str(i) + str(p))
	# 		break

	if( False ):
		print(False)
	else:
		# find keywords per title
		title = p[3].lower()
		# print( title )
		kfound = []
		for k in kw:
			if(title.__contains__(k[0])):
				kfound.append(k[0])
		if(len(kfound) <= 0): empties.append(p)
		# print(kfound)
		kfound = (';'.join(kfound))

		# find sections and ssid per main author
		# print(p[-2])
		try:
			pubAuthors = p[4].split(';') #[-2]
		except:
			print(p)
			break
		# print(pubAuthors[0])
		mainAuthor = pubAuthors[0].lower()
		aname = mainAuthor
		name = ''
		surname = ''
		if(mainAuthor == "aa. vv." or mainAuthor == "aa.vv." ):
			aname = "aa. vv."
			print("vari")
		else:
			names = mainAuthor.split(' ') # separate name and surname
			if(len(names)>=2):
				name = names[1]
				surname = names[0]
				if(names[0].__contains__('.')):
					name = names[0].replace('.','')
					surname = names[1]
				elif(names[1].__contains__('.')):
					name = names[1].replace('.','')
					surname = names[0]

				else:
					# print('strange name ' + mainAuthor )
					surname = names[1]
					# break
				# search = surname + ' ' + name
				search = surname
				for a in authors:
					if a=='':
						break
					name = a[1].lower()
					if(name.__contains__(search)):
						index  = authors.index(a)
						aname = authors[index][1]
						section = authors[index][5]
						ssid = authors[index][8]
						namesFound += 1
						# print('found surname-name ' + search)
						continue

						# search = name + ' ' + surname
						#
						# if(name.__contains__(search)):
						# 	index  = authors.index(a)
						# 	aname = authors[index][1]
						# 	section = authors[index][5]
						# 	ssid = authors[index][8]
						# 	namesFound += 1
						# 	print('found name-surname' + search)
						# 	break

			else:
				for a in authors:
					if a=='':
						break
					name = a[1].lower()
					if(name.__contains__(mainAuthor)):
						index  = authors.index(a)
						aname = authors[index][1]
						role = authors[index][5]
						section = authors[index][6]
						contract = authors[index][7]
						ssid = authors[index][8]
						namesFound += 1
						if mainAuthor=="": break
						print('found surname-name ' + mainAuthor)
						continue

				# print('single name ' + str(p[4]).replace('.',' '))
				# break
				# search = mainAuthor

		newpub = p[0:4]

		newpub.append(aname)
		newpub.append(section)
		newpub.append(ssid)
		newpub.append(kfound)
		records.append(newpub)
	i += 1
	if(stop>0):
		if(( i > stop ) or ( i < 0)): break

print("pubblication: " + str(i) + " of " + str( len(pubbs)))
print("empties: " + str( len(empties) ))
print("notValid: " + str( len(notValid) ))
print("keywords: " + str( len(kfound)))
print("names found: " + str( namesFound ))


# author, section, year, type, title, kw
newHeaders = headersPub[0:4]
newHeaders.append("dc.mainAuthor")
newHeaders.append("dc.section")
newHeaders.append("dc.ssid")
newHeaders.append("dc.keywords")



time  = datetime.now()
fileName = "kwAuthor_" + str(time.day) + "_" + str(time.month) + "_" + str(time.hour) + "_" + str(time.minute) + ".csv"

ofile = open(fileName,"w")
writer = csv.writer(ofile,delimiter=",")
i = 0
print("writing")
writer.writerow(newHeaders)
for rec in records:
	i += 1
	for w in rec:
		w.replace('\uf19d','')
		# print(w)
	try:
		writer.writerow(rec)
		# print("written")
	except:
		print("failed")
		print(str(rec))
		continue

print("Lines written " + str(i))
ofile.close()
