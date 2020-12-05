#works for all pages of one url
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import gc
import tracemalloc

# tracemalloc.start() #------Memory stuff

def scrapepage(pageurl, f):
	#Go to provided url
	uClient = uReq(pageurl)
	page_html = uClient.read()
	uClient.close()

	#Scrape page and find containers for job postings
	page_soup = soup(page_html, "html.parser") 
	containers = page_soup.findAll("div", {"data-tn-component":"organicJob"})

	for x in containers:
		f.write(
			x.div.div.span.text.strip().replace(",", "") 
			+ "," + x.a.text.strip().replace(",", "")
			+ "," + x.find("span", {"class":"location"}).text.replace(",", "")
			+ "," + link
			+ "\n"
		)

	#Determine current page, next page
	curr_page = page_soup.find("b", {"aria-current":"true"}).text
	next_page = int(curr_page) + 1

	#If next page exists, recursively scrape it
	if (page_soup.find("a", {"aria-label":next_page})):
		scrapepage("https://ca.indeed.com" + page_soup.find("a", {"aria-label":next_page}).get('href'), f)


#Creates CSV file
filename = "jobs.csv"
f = open(filename, "w")
headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
f.write(headers)

#Scraoes seed url and next pages
scrapepage('https://ca.indeed.com/jobs?q=software+developer+co-op&l=Canada', f)

f.close()

# Memory stuff
# gc.collect()
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tracemalloc.stop()