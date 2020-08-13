import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import json as JSON
from multiprocessing.pool import ThreadPool
import threading




threadLocal = threading.local()

def get_driver():
	driver = getattr(threadLocal, 'driver', None)
	if(driver is None):
		option = webdriver.ChromeOptions()
		option.add_argument("--headless")
		option.add_argument("--incognito")
		option.add_argument("--log-level=3")

		option.add_argument("user-agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'")

		driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=option)        
		setattr(threadLocal, 'driver', driver)

	return driver

def generate_urls():
	for page in range(1,6):
		product_page_url.append(BASE_URL+'+'.join(product_name.split())+f"&page={page}")



def scrape(page_url):
	driver = get_driver()

	driver.get(page_url)

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


		except:
			print("rejected")






if __name__ == '__main__':
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


	product_page_url = []

	product_json = []
	missing_values = 0
	generate_urls()

	# print(product_page_url)

	ThreadPool(5).map(scrape,product_page_url)


	with open(f"{product_name}.json", 'w', encoding='utf-8', errors='ignore') as f:
		JSON.dump(product_json, f, ensure_ascii=False, indent=4)

	print("Total Products Scraped ",len(product_json))


