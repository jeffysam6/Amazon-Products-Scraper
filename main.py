import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import json as JSON

pages = 6
BASE_URL = 'https://www.amazon.com/s?k='

while(True):
	print("Enter the product  to be Scraped")
	product_name = input()
	if(product_name):
		break
	else:
		print("Please Try Again!!")
		print()




option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--incognito")

option.add_argument("user-agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'")

driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=option)        


product_json = []

missing_values = 0



for page in range(1,pages):

	driver.get(BASE_URL+'+'.join(product_name.split())+f"&page={page}")

	req = driver.page_source

	page_html = soup(req,'html.parser')

	product_containers = page_html.find_all('div',class_="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32")

	per_page_product = 0
	rejected_per_page = 0

	for products in product_containers:
		json = {}
		try:
			image = products.find("img",class_='s-image')
			stars = products.find("span",class_='a-icon-alt')
			price = products.find('span',class_='a-offscreen')
			json['title'] = image['alt']
			json['image'] = image['src']
			json['ratings'] = stars.text
			json['price'] = price.text
			product_json.append(json)
			per_page_product += 1


		except:
			missing_values += 1
			rejected_per_page += 1

	print(f"*********** Page {page} ***********************")
	print("Products Scraped: ",per_page_product )
	print('Products Rejected: ',rejected_per_page)
	print()

driver.close()


with open(f"{product_name}.json", 'w', encoding='utf-8', errors='ignore') as f:
	JSON.dump(product_json, f, ensure_ascii=False, indent=4)







print()

print("Total Products Scraped ",len(product_json))

print("Total Products Rejected ",missing_values)



