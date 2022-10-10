from bs4 import BeautifulSoup
import urllib.request
import numpy

seed_url = "https://www.sec.gov/news/pressreleases"
fullText = False # if False, code returns snippet of body that contains 'charges'. if True, code returns entire body of page that contains 'charges'

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
charge = []
charge_text = []

maxNumUrl = 20; #set the maximum number of urls to visit
found = 0;
print("Starting with url="+str(urls))
while len(urls) > 0 and len(charge) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        # print("num. of URLs in stack: %d " % len(urls))
        # print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except Exception as ex:
        # print("Unable to access= "+curr_url)
        # print(ex)
        continue    #skip code below
    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if len(charge) < maxNumUrl:
            try:
                reqChild = urllib.request.Request(childUrl,headers={'User-Agent': 'Mozilla/5.0'})
                webpageChild = urllib.request.urlopen(reqChild).read()
                soupChild = BeautifulSoup(webpageChild);
                if "CHARGES" in soupChild.get_text().upper():
                    if childUrl not in charge:
                        charge.append(childUrl)
                        i_sub = max(soupChild.get_text().upper().index("CHARGES")-50,0)
                        subtext = soupChild.get_text()[i_sub:(i_sub+100)]
                        if fullText:
                            charge_text.append(soupChild.get_text())
                        else :
                            charge_text.append(subtext)
                        found = found + 1
                        print("Found %d 'charges' urls" % (found))
            except Exception as ex:
                continue

            if seed_url in childUrl and childUrl not in seen:
            # print("***urls.append and seen.append***")
                urls.append(childUrl)
                seen.append(childUrl)
                
print("'charges' urls:")
for i in numpy.arange(0,len(charge),1):
    print("\t URL:")
    print(charge[i])
    print("\t 'charges' Text snippet:")
    print(charge_text[i])
