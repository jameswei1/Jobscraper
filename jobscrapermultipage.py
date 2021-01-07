#works for all pages of one url
from urllib.request import urlopen as uReq, Request
from bs4 import BeautifulSoup as soup 
import gc
import tracemalloc
# tracemalloc.start() #------Memory stuff

def scrapepageindeed(pageurl, f):
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
			+ "," + 'https://ca.indeed.com' + x.a.get('href')
			+ "\n"
		)

	#Determine current page, next page
	curr_page = page_soup.find("b", {"aria-current":"true"}).text
	next_page = int(curr_page) + 1

	#If next page exists, recursively scrape it
	if (page_soup.find("a", {"aria-label":next_page})):
		scrapepageindeed("https://ca.indeed.com" + page_soup.find("a", {"aria-label":next_page}).get('href'), f)

def scrapepageglassdoor(pageurl, g):
	#Go to provided url
	req = Request(pageurl, headers = {'User-Agent': 'Mozilla/5.0'})
	uClient = uReq(req)
	page_html = uClient.read()
	uClient.close()

	#Scrape page and find containers for job postings
	page_soup = soup(page_html, "html.parser")
	

#Creates indeed CSV file
filenameindeed = "indeedjobs.csv"
f = open(filenameindeed, "w")
headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
f.write(headers)

#Creates glassdoor CSV file
filenameglassdoor = "glassdoorjobs.csv"
g = open(filenameglassdoor, "w")
headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
g.write(headers)

#Scraoes seed url and next pages
#scrapepageindeed('https://ca.indeed.com/jobs?q=software+developer+co-op&l=Canada', f)
scrapepageglassdoor('https://www.glassdoor.ca/Job/software-developer-co-op-jobs-SRCH_KO0,24.htm', g)

f.close()
g.close()

# Memory stuff
# gc.collect()
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tracemalloc.stop()