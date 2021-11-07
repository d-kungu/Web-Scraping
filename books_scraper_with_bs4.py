''' Web Scrapper for collecting data from e-commerce like webpage
 https://books.toscrape.com/ a dummy website for practicing web crawling.

Written by: Diana Kung'u

'''

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

all_books = []


# Function that  loads page and return all listed books details
def page(url):
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    return soup.find_all("article", attrs={"class": "product_pod"})


#Function that extract required information from each listing
def extract(listings):
    for listing in listings:
        base_link = "http://books.toscrape.com/catalogue/"
        link = listing.find("a").get("href")
        book_link = base_link + link # create product list link
       
        # get the link of each product
        book_page = requests.get(book_link)
        soup_2 = bs(book_page.text, "lxml")

        # title
        book_info = soup_2.find("div", attrs={"class": "col-sm-6 product_main"})
        title = book_info.find("h1").text

        # price
        price = book_info.find("p").text.strip()[2:]

        # upc
        upc = soup_2.find("td").text

        book = {"title": title, "price": price, "upc": upc}
        all_books.append(book)
    


pg = 1 # initialize page numbers

while True: # Loop through all pages on the site
    url = f"http://books.toscrape.com/catalogue/page-{pg}.html"
    print(f"extracting page {pg}")
    listings = page(url)
    if len(listings) == 0: #Terminate if page has no product listings

        break
    else:
        extract(listings)
        pg += 1


df = pd.DataFrame(all_books)
print(df)
print(df.shape)
