#!/usr/bin/python3
import threading, time, re, MySQLdb 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from dd_individual import scrapeListing
from decimal import Decimal


#Create new .csv file for results
filename = "donedeal_vehicles.csv"
f_results = open(filename, "w", encoding='utf-8')
f_results.write("title, price, year, engine, mileage, posted, county, listing_url, image_url\n")

#Create new .csv file for results
filename = "donedeal_individual.csv"
f_individual = open(filename, "w", encoding='utf-8')
f_individual.write("key, value\n")

exitFlag = 0

#Declare class myThread
class myThread (threading.Thread):
	#Initialise class (i.e. the constructor)
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name + " " + str(time.ctime())) #Declare thread name and start-time
      print_time(self.name, self.counter) #Call print_time() method
      print ("Exiting " + self.name + " " + str(time.ctime())) #Declare thread name and finish-time
	  

def print_time(threadName, counter):
	for x in range(counter, 71000, 448):
		url = "https://www.donedeal.ie/cars/" + "?start=" + str(x)
		uClient = uReq(url)#Opening the connection, storing the page HTML, closing the connection
		html = uClient.read()
		uClient.close()
		dd_soup = soup(html, "html.parser")#Parse this iteration's HTML with BeautifulSoup
		
		containers = dd_soup.findAll("li", {"class":"card-item"})#Store the HTML of each listing card in an array called containers

		for container in containers:#Loop through all containers, extracting necessary data. 
			try:#Enclosed in try-catch block, which will ignore irrelevant advertising
			
				title_container = container.findAll("p", {"class":"card__body-title"})#Extract vehicle title
				title = title_container[0].text
				
				price_container = container.findAll("p", {"class":"card__price"})#Extract price
				price = str(price_container[0].span.text)
				if(price != "No Price"):
					price = Decimal(re.sub(r'[^\d.]', '', price))
				else:
					price = 0

				card_href_container = container.find("a", {"class":"card__link"})#Extract the URL of each listing
				card_href = card_href_container.attrs["href"]
				
				card_media_container = container.find("div", {"class":"card__photo"})#Extract image URL of each listing
				image_url_container = card_media_container.find("img",{"data-lazy-img":True})
				image_url = image_url_container.attrs["data-lazy-img"]
				
				info_container = container.find("ul", {"card__body-keyinfo"})#Extract key info
				info = info_container.findAll("li")
				if len(info) == 5:#Items are stored in consistent order in a "ul". Loop to extract
					year = info[0].text
					engine = info[1].text
					mileage = info[2].text
					posted = info[3].text
					county = info[4].text
				elif len(info) == 4:#If mileage is missing, replace with "Undisclosed" 
					year = info[0].text
					engine = info[1].text
					mileage = 0
					posted = info[2].text
					county = info[3].text
				else:
					break

					
				#Call scrapeListing() function from dd_individual file
				scrapeListing(card_href, price, posted, card_href, image_url)
				
				#Print extracted values to console
				#print("Vehicle title: ",  title, "\nPrice: ",  price, "\nYear: ",  year, "\nEngine: ",  engine, "\nMileage: ",  mileage, "\nPosted: ",  posted, "\nCounty: ",  county, "\nHREF: ",  card_href, "\nImage URL: ",  image_url)
				
				#Write values to the .csv file. These files' cells are deliminated by a comma, so replace all commas in extracted falues with pipes ("|")
				f_results.write(title.replace(",", "|") + "," + str(price) + "," + year.replace(",", "|") + "," + engine.replace(",", "|") + "," + mileage.replace(",", "|") + "," + posted.replace(",", "|") + "," + county.replace(",", "|") + "," + card_href.replace(",", "|") + "," + image_url.replace(",", "|") +"\n")
							
			except AttributeError:
				pass

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 28)
thread3 = myThread(3, "Thread-3", 56)
thread4 = myThread(4, "Thread-4", 84)
thread5 = myThread(5, "Thread-5", 112)
thread6 = myThread(6, "Thread-6", 140)
thread7 = myThread(7, "Thread-7", 168)
thread8 = myThread(8, "Thread-8", 196)
thread9 = myThread(9, "Thread-9", 224)
thread10 = myThread(10, "Thread-10", 252)
thread11 = myThread(11, "Thread-11", 280)
thread12 = myThread(12, "Thread-12", 308)
thread13 = myThread(13, "Thread-13", 336)
thread14 = myThread(14, "Thread-14", 364)
thread15 = myThread(15, "Thread-15", 392)
thread16 = myThread(16, "Thread-16", 420)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
thread11.start()
thread12.start()
thread13.start()
thread14.start()
thread15.start()
thread16.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()
thread11.join()
thread12.join()
thread13.join()
thread14.join()
thread15.join()
thread16.join()

print ("Exiting Main Thread")
f_results.close()
f_individual.close()
