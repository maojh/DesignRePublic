import sys
import csv
from datetime import datetime, date, timedelta
import requests,re
from bs4 import BeautifulSoup

print "starting"
reload(sys)
sys.setdefaultencoding('utf8')


content  = []
record = []
url = ""

failedRequests = []

# argv`get url file
argv = sys.argv[1:]

origin = argv[0]
print origin

count = 0

# return the title from the list of fields
def getValue(fields,attr):
    for x in fields:
        # if it's a attr field
        if x.getText().__contains__(attr)==True:
            # return the content of the corresponding field value
            return values[fields.index(x)].getText()

def getAuthors(fields):
    authors = []
    for x in fields:
        # if it's a attr field
        if x.getText().__contains__("Autori")==True:
            v = values[fields.index(x)]
            for c in v.children:
                if not(c.getText().__contains__("esterni")):
                    author = c.getText()
                    author = author.replace(',','')
                    author = author.capitalize()
                    authors.append(author)
    authors = reduce(lambda x,y: x+";"+y,authors)
    return authors

with open(origin,"rb") as f:
    reader = csv.reader(f,delimiter=",")
    # next(reader, None)
    for u in reader:
        count += 1
        print ""
        print "Line count ", count
        print ""

        record = []
        url = u[0]
        print url

        if url == "":
            url = "https://re.public.polimi.it/handle/11311/1000419"

        try:
            r = requests.get(url)
            print r.status_code
            r.raise_for_status()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            failedRequests.append(url)
            print e
            break

        html = "".join(line.strip() for line in r.content.split("/n"))
        soup = BeautifulSoup(html,'lxml')

        fields = soup.findAll("td",{"class":"metadataFieldLabel"})
        values = soup.findAll("td",{"class":"metadataFieldValue"})

        if fields==[]:
            failedRequests.append(url)
            print "nonvalid request"
            # break
        else:

            authors = soup.findAll('a',{"class":"author"})
            contributors = soup.findAll('div',{"class":"contributor"})
            internCont = soup.findAll('div',{"class":"internalContributor"})
            externCont = soup.findAll('div',{"class":"externalContributor"})

            title = getValue(fields,"Titolo")
            title = title.replace("\n"," ").replace("\r"," ").capitalize()
            year =  getValue(fields,"Data di pubblicazione")
            authors = getAuthors(fields)

            # For each element in contributors get name, remove the comma and capitalize first letter
            # authors = list(map(lambda x: x.getText().capitalize(), contributors))
            # authors = map(lambda x: x.replace(',',''),authors)
            # authors = filter(lambda x: not(x.__contains__("autori esterni")),authors)
            # authors = reduce(lambda x,y: x+";"+y,authors)

            # internalAuthors = list(map(lambda x: x.getText().capitalize(), internCont))
            # internalAuthors = map(lambda x: x.replace(',',''),internalAuthors)
            # internalAuthors = filter(lambda x: not(x.__contains__("autori esterni")),internalAuthors)
            # internalAuthors = reduce(lambda x,y: x+";"+y,internalAuthors)

            record.append(title)
            record.append(year)
            record.append(authors)
            # record.append(internalAuthors)
            #
            # if len(externCont)>0:
            #     externalAuthors = list(map(lambda x: x.getText().capitalize(), externCont))
            #     externalAuthors = map(lambda x: x.replace(',',''),externalAuthors)
            #     externalAuthors = filter(lambda x: not(x.__contains__("autori esterni")),externalAuthors)
            #     externalAuthors = reduce(lambda x,y: x+";"+y,externalAuthors)
            #     record.append(externalAuthors)
            # else:
            #     externalAuthors = "-"

            print record

            content.append(record)
            # break

# csv writer output

time  = datetime.now()

fileName = "data_" + str(time.hour) + "_" + str(time.minute) + ".csv"

ofile = open(fileName,"wb")

writer = csv.writer(ofile,delimiter=",")
# writer.writerow(['title','year','authors','internalAuthors','externalAuthors'])
writer.writerow(['title','year','authors'])
writer.writerows(content)

ofile.close()
