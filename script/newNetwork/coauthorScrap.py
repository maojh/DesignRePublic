import sys
import csv
import datetime
import requests,re
from bs4 import BeautifulSoup

record = []
url = ""

# argv`get url file



if url == "":
    url = "https://re.public.polimi.it/handle/11311/1004058?mode=simple.593"

r = requests.get(url)
print r.status_code

html = "".join(line.strip() for line in r.content.split("/n"))
soup = BeautifulSoup(html,'lxml')

fields = soup.findAll("td",{"class":"metadataFieldLabel"})
values = soup.findAll("td",{"class":"metadataFieldValue"})


# return the title from the list of fields
def getValue(fields,attr):
    for x in fields:
        # if it's a title field
        if x.getText().__contains__(attr)==True:
            # return the content of the corresponding field value
            return values[fields.index(x)].getText()

contributors = soup.findAll('div',{"class":"contributor"})
# For each element in contributors get name, remove the comma and capitalize first letter
title = getValue(fields,"Titolo")
year =  getValue(fields,"Data di pubblicazione")
authors = list(map(lambda x: x.getText().replace(',','').capitalize(), contributors))


record.append(title)
record.append(year)
record.append(authors)

# csv writer output
for r in record:
    print r
