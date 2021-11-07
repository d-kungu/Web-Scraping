'''
A simple python Script that extracts Exchange Rate from 
https://open.er-api.com/v6 Endpoint.
- Connects to API
- Extract Data
- Parse Json and create Dataframe

   ** Created by: Diana Kung'u **

'''
import json
import requests
from pandas import read_json, DataFrame, Series


#Input a currency
base_currency = input('Please enter the base currency')
convert_to = input('Please enter the currency to convert to')
try:
# Connect to  API
    response = requests.get(f"https://open.er-api.com/v6/latest/{base_currency.upper()}")
    # get Rate
    rates = response.json()['rates']
    converted = rates.get(convert_to.upper())

    if converted == None:
        print("Please enter a valid convert to currency")
    else:
        print(f'1 unit of {base_currency} is equal to {convert_to} : {converted}') 
    
except:
   print("Invalid: base currency")

# 



