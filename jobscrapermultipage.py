#works for all pages of one url
from urllib.request import urlopen as uReq, Request
from bs4 import BeautifulSoup as soup 
import threading
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
		link = 'https://ca.indeed.com' + x.a.get('href')
		f.write(
			x.div.div.span.text.strip().replace(",", "") 
			+ "," + x.a.text.strip().replace(",", "")
			+ "," + x.find("span", {"class":"location"}).text.replace(",", "")
			+ "," + '=HYPERLINK("' + link + '")'
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
	article = page_soup.findAll("article", {"id":"MainCol"})
	jobs = article[0].div.ul.find_all("li")

	for x in jobs:
		try:
			link = 'https://www.glassdoor.ca' + x.find("a", {"class":"jobInfoItem jobTitle css-13w0lq6 eigr9kq1 jobLink"}).get('href')
			g.write(
				x.find("a", {"class":"css-10l5u4p e1n63ojh0 jobLink"}).text.replace(",", "")
				+ "," + x.find("a", {"class":"jobInfoItem jobTitle css-13w0lq6 eigr9kq1 jobLink"}).text.replace(",", "")
				+ "," + x.find("div", {"class":"d-flex flex-wrap css-yytu5e e1rrn5ka1"}).span.text.replace(",", "")
				+ "," + '=HYPERLINK("' + link + '")'
				+ "\n"
			)
		except AttributeError:
		 	g.write("\nTerminating due to AttributeError\n")
		 	return

		
	if (page_soup.find("li", {"class":"next"})):
		scrapepageglassdoor("https://www.glassdoor.ca" + page_soup.find("li", {"class":"next"}).a.get('href'), g)

#Creates indeed CSV file
# filenameindeed = "indeedjobs.csv"
# f = open(filenameindeed, "w")
# headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
# f.write(headers)

#Creates glassdoor intern CSV file
# filenameglassdoorintern = "glassdoorinternjobs.csv"
# g = open(filenameglassdoorintern, "w")
# headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
# g.write(headers)

#Creates glassdoor fulltime CSV file
filenameglassdoorfulltime = "glassdoorfulltimejobs.csv"
h = open(filenameglassdoorfulltime, "w")
headers = "Company-Name, Job-Title, Location, Link-To-Apply\n"
h.write(headers)

#Multithreading
# t1 = threading.Thread(target=scrapepageindeed, args=('https://ca.indeed.com/jobs?q=software+developer+co-op&l=Canada', f,))
# t2 = threading.Thread(target=scrapepageglassdoor, args=('https://www.glassdoor.ca/Job/software-developer-co-op-jobs-SRCH_KO0,24.htm?jobType=internship', g,))
t3 = threading.Thread(target=scrapepageglassdoor, args=('https://www.glassdoor.ca/Job/software-developer-co-op-jobs-SRCH_KO0,24.htm?jobType=fulltime', h,))

# t1.start()
# t2.start()
t3.start()

# t1.join()
# t2.join()
t3.join()

#Closes file pointers
# f.close()
# g.close()
h.close()

# Memory stuff
# gc.collect()
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tracemalloc.stop()