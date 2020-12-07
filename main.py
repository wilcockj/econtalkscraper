from gazpacho import get, Soup
import requests
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm
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
    print(items)
    itemlist = []
    for item in items:
        itemdict = {}
        itemdict['url'] = item.find('guid').contents
        itemdict['title'] = item.find('title').contents
        date = item.find('pubdate').contents
        #2006-16-Mar-Title.mp3
        date = date[0].split()
        date = f"{date[3]}-{date[1]}-{date[2]}"
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
                infolist.append([row[0].lstrip("['").rstrip("']"),row[1].lstrip("['").rstrip("']"),row[2]])
            linecount += 1
    return infolist
def downloadpodcast(data):
    for item in tqdm(data):
        r = requests.get(item[0])
        #2006-16-Mar-Title.mp3
        open(f"downloads/{item[2]}-{item[1]}.mp3","wb").write(r.content)
#podcasts = parsexml('econtalk.xml')
#print(podcasts)
#writetocsv(podcasts,'econ.csv')
data = loadcsv('econ.csv')
downloadpodcast(data)
mp3 = getmp3('https://www.econtalk.org/rob-wiblin-and-russ-roberts-on-charity-science-and-utilitarianism/')
