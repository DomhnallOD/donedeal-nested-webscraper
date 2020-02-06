from urllib.request import urlopen as uReq, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup as soup
import json, re, time
from decimal import Decimal
import MySQLdb

'''
Create new .csv file 
'''
filename = "donedeal_individual.csv"
f_individual = open(filename, "w", encoding='utf-8')
f_individual.write("title, price, description, make, model, year, mileage, fuel type, transmission, body type, engine size, road tax, previous owners, country of origin, colour, doors\n")


'''
Define function to scrape all details from the individual listing 
'''
def scrapeListing(listingUrl, price, posted, card_href, image_url):

	from urllib.request import urlopen as uReq, Request
	from urllib.parse import urlencode
	from bs4 import BeautifulSoup as soup
	import json, re, time

	title = "undisclosed"
	description = "undisclosed"
	make = "undisclosed"
	model = "undisclosed"
	year = 0
	value = 0
	mileage = 0
	fuel_type = "undisclosed"
	transmission = "undisclosed"
	body_type = "undisclosed"
	engine_size = "undisclosed"
	road_tax = 0
	country_of_origin = "undisclosed"
	colour = "undisclosed"
	doors = 0
	owners = 0
	telephone = 0
	
	'''
	Opening the connection, storing the page HTML, closing the connection, creating page soup
	'''
	url = listingUrl 
	uClient = uReq(url)
	html = uClient.read()
	uClient.close()
	soup = soup(html, "html.parser")
	'''
	Extract title
	'''
	title = soup.find("title").text
	x = title.find("for sale in")#Trim from "for sale in"
	title = title[:x]
	#f_individual.write("Title, " + title.replace(",", "|") + "\n")

	'''
	Extract description
	'''
	desc = soup.find("meta", {"name":"description"})
	desc = desc["content"]
	#f_individual.write("Description," + desc.replace(",", "|") + "\n")
	'''
	Extract data from "Key Info" section
	'''
	data = str(soup.find_all('script', text=re.compile('window.adDetails')))
	x = data.find('"displayAttributes"')+20#Get start index of the "displayAttributes" string, + 20 is start of JSON list
	r = data[x:]#Strip previous characters
	x = r.find(']')+1#Find index of first "]" + 1, marking end of JSON object
	infolist = r[:x]
	obj = json.loads(infolist)#Strip subsequent characters, convert to JSON object
	info = []
	#print(obj)
	
	for i in range(len(obj)):
		if(obj[i]["name"] == "make"):
			make = obj[i]["value"].lower()
		elif obj[i]["name"] == "model":
			model = obj[i]["value"].lower()
		elif obj[i]["name"] == "year":
			year = int(obj[i]["value"])
		elif obj[i]["name"] == "mileage":
			if obj[i]["value"] == "":
				mileage = 0
			else:
				mileage = Decimal((re.sub(r'[^\d.]', '', obj[i]["value"])))			
		elif obj[i]["name"] == "transmission":
			if obj[i]["value"] == "":
				transmission = "manual"
			else:
				transmission = obj[i]["value"].lower()
		elif obj[i]["name"] == "bodyType":
			body_type = obj[i]["value"].lower()
		elif obj[i]["name"] == "engine":
			if obj[i]["value"] == "":
				engine_size = 0
			else:
				engine_size = Decimal((re.sub(r'[^\d.]', '', obj[i]["value"])))	
		elif obj[i]["name"] == "roadTax":
			if road_tax != 0:
				road_tax = obj[i]["value"]
			else:
				road_tax = "0"
			
		elif obj[i]["name"] == "previousOwners":
			if obj[i]["value"] == "":
				owners = 0
			else:
				owners = int((re.sub(r'[^\d.]', '', obj[i]["value"])))			
		elif obj[i]["name"] == "country":
			country_of_origin = obj[i]["value"].lower()
		elif obj[i]["name"] == "colour":
			colour = obj[i]["value"].lower()
		elif obj[i]["name"] == "numDoors":
			if obj[i]["value"] == "":
				doors = 0
			else:
				doors = int((re.sub(r'[^\d.]', '', obj[i]["value"])))			
		elif obj[i]["name"] == "fuelType":
			fuel_type = obj[i]["value"].lower()


	'''
	Extract phone number by making separate post request to DoneDeal API
	'''
		
	json_start = data.find('window.adDetails = {')+19
	json_sect = data[json_start:]
	json_end = json_sect.find("}};")+2
	json_obj = json.loads(json_sect[:json_end])#Strip subsequent characters, convert to JSON object
	id = str(json_obj["id"])#This is the ID of the listing
	tel_url = "https://www.donedeal.ie/cadview/api/v3/view/ad/" + id + "/phone/"
	post_fields = {'foo': 'bar'}
	request = Request(tel_url, urlencode(post_fields).encode())#Make post request to DoneDeal.ie API
	tel_response = uReq(request).read().decode()#Decode response
	tel_obj = json.loads(tel_response)#This produces a valid JSON object
	telephone = tel_obj["phone"]
	f_individual.write(telephone)

	'''
	Write data to csv file
	'''
	f_individual.write(title.replace(",", "|") + "," + str(price) + "," + desc.replace(",", "|") + "," + make.replace(",", "|") + "," + model.replace(",", "|") + "," + str(year) + "," + str(mileage) + "," + fuel_type.replace(",", "|") + "," + transmission.replace(",", "|") + "," + body_type.replace(",", "|") + "," + str(engine_size) + "," + road_tax.replace(",", "|") + "," + str(owners) + "," + country_of_origin.replace(",", "|") + "," + colour.replace(",", "|") + "," + str(doors) +"\n")
	
	#The following function has been disabled as DB is no longer hosted
	'''
	Make post to DB 

	connection = MySQLdb.connect (host = "mysql1.it.nuigalway.ie", user = "mydb4692dd", passwd = "zy7row", db = "mydb4692")
	connection.set_character_set('utf8mb4')
	cursor = connection.cursor()
	cursor.execute ("INSERT INTO WEBSCRAPE_LISTING(title, description, make, model, price, year, engine_size, engine_type, km, posted, county, listing_href, image_url, body, previous_owners, colour, transmission, doors) VALUES ('" + title.replace("'", "|") + "','" + desc.replace("'", "|") + "','" + make + "','" + model + "','" + str(price) + "','" + str(year) + "','" + str(engine_size) + "','" + fuel_type + "','" + str(mileage) + "','" + posted + "','" + county + "','" + card_href + "','" + image_url + "','" + body_type + "','" + str(owners) + "','" + colour + "','" + transmission + "','" +  str(doors) + "')")

	connection.commit()
	cursor.close()
	connection.close()
	'''
	
	'''
	Log to console
	'''
	atomic_listing = "    ____\n __/  |_\_\n|  _     _``-.\n'-(_)---(_)--'" +  "\nVehicle title: \t" +  title + "\nDescription: \t" +  description + "\nMake: \t\t" + make + "\nModel: \t\t" + model + "\nValue: \t\t" + str(value) + "\nYear: \t\t" +  str(year) + "\nEngine Size: \t" +  str(engine_size) + "\nFuel Type: \t" + fuel_type + "\nTransmission: \t" + transmission + "\nBody Type: \t" + body_type + "\nMileage: \t" +  str(mileage) + "\nPosted: \t" +  "\nRoad Tax: \t" + str(road_tax) + "\nColour: \t" + colour + "\nDoors: \t\t" + str(doors) +	"\nTelephone: \t"+ telephone + "\n\n"
	print(atomic_listing)
	
	
	'''
	Extract photo URLs
	'''
	photos_start = data.find('"photos":[{')+9#Get start index of the ""photos":[{" string, + 9 is start of image url list
	images_sect = data[photos_start:]#Strip previous characters
	images_end = images_sect.find('"}],')+3#Find index of first ""}]," + 3, marking end of JSON object
	images_obj = json.loads(images_sect[:images_end])#Strip subsequent characters, convert to JSON object
	images = []
	for group in range(len(images_obj)):#Loop each URL value into a list "images"
		images.append(images_obj[group]["medium"])
	for src in range(len(images)):
		asdfgh=0
		#f_individual.write("Image," + images[src] + "\n")
		
	


	

