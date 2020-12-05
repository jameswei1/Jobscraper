#works for all pages of one url

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import gc
import tracemalloc

# tracemalloc.start() #------Memory stuff

def scrapepage(pageurl, f):
	uClient = uReq(pageurl)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser") 

	containers = page_soup.findAll("div", {"data-tn-component":"organicJob"})

	for x in containers:
		#Unnecessary prints for debugging
		print("Company-Name: " + x.div.div.span.text.strip())
		print("Job-Title: " + x.a.text.strip())
		print("Location: " + x.find("span", {"class":"location"}).text)
		link = 'https://ca.indeed.com' + x.a.get('href')
		print("Link-To-Apply: " + link)
		print("-------------------------------------------------")

		f.write(
			x.div.div.span.text.strip().replace(",", "") 
			+ "," + x.a.text.strip().replace(",", "")
			+ "," + x.find("span", {"class":"location"}).text.replace(",", "")
			+ "," + link
			+ "\n"
		)

	curr_page = page_soup.find("b", {"aria-current":"true"}).text
	next_page = int(curr_page) + 1

	if (page_soup.find("a", {"aria-label":next_page})):
		scrapepage("https://ca.indeed.com" + page_soup.find("a", {"aria-label":next_page}).get('href'), f)

#------------------------------------------------------------------------------------------end of function

#Sets seed URL
myURL1 = 'https://ca.indeed.com/jobs?q=software+developer+co-op&l=Canada'

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