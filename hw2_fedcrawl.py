from bs4 import BeautifulSoup
import urllib.request

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
covid_url = []

maxNumUrl = 10; #set the maximum number of urls to visit
found = 0;
print("Starting with url="+str(urls))
while len(urls) > 0 and len(covid_url) < maxNumUrl:
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
        if len(covid_url) < maxNumUrl:
            try:
                reqChild = urllib.request.Request(childUrl,headers={'User-Agent': 'Mozilla/5.0'})
                webpageChild = urllib.request.urlopen(reqChild).read()
                soupChild = BeautifulSoup(webpageChild);
                if "COVID" in soupChild.get_text().upper():
                    if childUrl not in covid_url:
                        covid_url.append(childUrl)
                        found = found + 1
                        print("Found %d COVID urls" % (found))
            except Exception as ex:
                continue

            if seed_url in childUrl and childUrl not in seen:
            # print("***urls.append and seen.append***")
                urls.append(childUrl)
                seen.append(childUrl)
                
print("COVID urls:")
for covid in covid_url:
    print(covid)
