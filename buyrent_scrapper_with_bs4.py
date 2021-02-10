import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from requests.models import Response

all_houses = []


def all_listings(url):
    res = requests.get(url)
    status = res.status_code
    house_soup = bs(res.text, "lxml")
    return [
        house_soup.find_all(
            "div", class_="flex flex-col items-stretch w-full px-2 pb-2 mt-2 lg:mt-0"
        ),
        status,
    ]


def extract(listings):
    for listing in listings:
        bed_rms = listing.find("span", {"data-cy": "card-beds"}).text.strip()
        try:
            sq_footage = listing.find("span", {"data-cy": "card-area"}).text.strip()
        except:
            sq_footage = ""
        try:
            location = listing.find_all("p")[1].text.strip()

        except:
            location = ""
        try:

            agency = listing.find("div", "inline-block mr-1").a["agency-slug"]
        except:
            agency = ""

        try:
            agent = listing.find("div", class_="flex justify-end space-x-7").div[
                "data-bi-listing-agent"
            ]
        except:
            agent = ""
        try:
            category = listing.find("div", class_="flex justify-end space-x-7").div[
                "data-bi-listing-category"
            ]
        except:
            category = ""
        try:
            offer_type = listing.find("div", class_="flex justify-end space-x-7").div[
                "data-bi-listing-offer-type"
            ]
        except:
            offer_type = ""

        try:
            rent = listing.find("p").text.strip()
        except:
            rent = ""

        house = {
            "no_bedrms": bed_rms,
            "location": location,
            "agency": agency,
            "agent": agent,
            "offer_type": offer_type,
            "size": sq_footage,
        }
        all_houses.append(house)


condition = True
pg = 106
while condition:
    url = f"https://www.buyrentkenya.com/houses-for-rent?page={pg}"
    print(f"scraping page {pg}")
    if all_listings(url)[1] == 200:
        listings = all_listings(url)[0]
        extract(listings)
        pg += 1
    else:
        break

df = pd.DataFrame(all_houses)
print(df.shape)
