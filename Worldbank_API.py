
'''Collecting data from World Bank API 
- Proportion number of people living in urban areas SP.URB.TOTL.IN.ZS 2010 - 2020
- https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
- Output: https://github.com/diana-kungu/Web-Scraping/blob/main/Data/WB_urban_population.csv
    ** Created by Diana Kung'u **

'''
import requests
import pandas as pd
import json



#1. Connect to the API
url = "http://api.worldbank.org/V2/country/all/indicator/SP.URB.TOTL.IN.ZS?format=json&date=2010:2020"
request = requests.get(url)
print(request.status_code) # 200 Status indicates successful connection

#2 Pull the data from the connection
data = request.text

#3 Parse data into JSON format & get number of pages
data =json.loads(data)
pages = data[0].get('pages')



pg = 1 #Initialize page numbers
results = []


#Loop through all pages and extract data
while pg <= pages:
    url = f"http://api.worldbank.org/V2/country/all/indicator/SP.URB.TOTL.IN.ZS?format=json&date=2010:2020&page={pg}"
    request = requests.get(url)
    data = json.loads(request.text)
    results.extend(data[1])
    pg += 1


#Parse list of nested dictionaries to create a dataframe
df =pd.json_normalize(results) 


#Reshape dataframe to have each country on one row and years on columns
df.drop(['indicator.value', 'indicator.id', 'decimal', 'obs_status', 'unit'], axis= 1, inplace= True)
df = df.pivot(index=['countryiso3code','country.id', 'country.value'], columns='date').reset_index()


df.columns = [' '.join(col).strip() for col in df.columns.values]

#OUTPUT DATA
df.to_csv(r'.\Data\WB_urban_population.csv', index = False)


