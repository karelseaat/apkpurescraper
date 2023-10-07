import requests
from bs4 import BeautifulSoup
import gzip

allcollectionfiles = []
allplaystoreappids = []
allplaystorelinks = set()

result = requests.get("https://play.google.com/robots.txt")

sitemaps = [n for n in result.text.strip("\n").split()[-3:] if "http" in n]

for n in sitemaps:
    results = requests.get(n)
    soup = BeautifulSoup(results.text, 'lxml')
    elements = soup.find_all('loc')
    
    for a in elements:
        allcollectionfiles.append(a.get_text())



for idx, onecol in enumerate(allcollectionfiles):
    result = requests.get(onecol)
    try:
        soup = BeautifulSoup(gzip.decompress(result.content), "lxml")
    except Exception:
        soup = BeautifulSoup("", "lxml")
    
    print(f"result list length: {len(list(allplaystorelinks))}, index of source list: {idx} of {len(allcollectionfiles)}")
        
    for link in  soup.find_all('xhtml:link'):
        temp = link['href']
        if "apps" in temp:
            temp2 = temp.split("/")[-1]
            if "=" in temp2:
                allplaystorelinks.add(temp2.split("=")[-1])




with open("resultfile.txt","w") as f:
    for link in allplaystorelinks:
        f.write(f"{link}\n")
