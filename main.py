from gazpacho import get, Soup
import requests
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import os
def getmp3(url):
    html = get(url)
    soup = Soup(html)
    mp3 = soup.find('audio')
    return mp3.text
def getxml(url):
   resp = requests.get(url) 
  
    # saving the xml file 
   with open('econtalk.xml', 'wb') as f: 
       f.write(resp.content) 
def parsexml(filename):
    with open(filename, 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content, "lxml")
    items = soup.findAll('item')
    itemlist = []
    for item in items:
        itemdict = {}
        itemdict['url'] = item.find('guid').contents
        itemdict['title'] = item.find('title').contents
        date = item.find('pubdate').contents
        date = date[0].split()
        date = f"{date[3]}-{date[2]}-{date[1]}"
        itemdict['date'] = date
        itemlist.append(itemdict)
    return itemlist
def writetocsv(items,filename):
    fields = ['url','title','date']

    with open(filename,'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames = fields)
        writer.writeheader()
        writer.writerows(items)
def loadcsv(filename):
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        linecount = 0
        infolist = []
        for row in csv_reader:
            if linecount != 0:
                charlist = ['"','[',']','\'']
                url = re.sub("|".join(charlist),"",row[0])
                url = url[1:-1]
                title = re.sub("|".join(charlist),"",row[1])
                title = title[1:-1]
                date = row[2]
                infolist.append([url,title,date])
            linecount += 1
    return infolist
def downloadpodcast(data):
    if os.pathexists('progress.txt'):
        with open('progress.txt', 'r') as f:
            start = int(f.readline())
    else:
        start = 0
    counter = start
    for item in tqdm(data[start:]):
        r = requests.get(item[0])
        #2006-16-Mar-Title.mp3
        open(f"downloads/{item[2]}-{item[1]}.mp3","wb").write(r.content)
        open(f"progress.txt","w").write(str(counter))
        counter += 1
podcasts = parsexml('econtalk.xml')
#print(podcasts)
writetocsv(podcasts,'econ.csv')
data = loadcsv('econ.csv')
downloadpodcast(data)
