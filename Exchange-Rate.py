'''
A simple python Script that extracts Exchange Rate from 
https://open.er-api.com/v6 Endpoint.
- Connects to API
- Extract Data
- Parse Json and create Dataframe
-Creates streamlit web App

   ** Created by: Diana Kung'u **

'''

import json
import requests
from pandas import read_json, read_csv
import streamlit as st
from datetime import datetime


#Currency List
currency_df = read_csv(r"https://raw.githubusercontent.com/datasets/currency-codes/master/data/codes-all.csv",
                       usecols=[0,1,2])
currency_df.dropna(how='any', inplace= True)
currency_df.drop_duplicates(keep='first', inplace= True, subset=['Entity', 'AlphabeticCode']) 
currency_codes = set(currency_df['AlphabeticCode'])

st.title("Currency Converter")

base_currency = st.selectbox("Select Currency From", currency_codes)
amount = st.number_input('Enter Amount')
convert_to  = st.selectbox("Select Currency To", currency_codes.difference({base_currency}))


def xchange_fnc(from_currency, to_currency):
#Connect to  API
    response = requests.get(f"https://open.er-api.com/v6/latest/{base_currency.upper()}")
    # get Rate
    global converted
    try:
        rates = response.json()['rates']
        rate = rates.get(convert_to.upper())
        converted = rates.get(convert_to.upper()) * amount
        st.write(f'1 unit of {base_currency} = {convert_to} : {convert_to+" "+ str(rate)} \
                    {(datetime.now().replace(second=0, microsecond=0)).strftime(format= "%Y-%m-%d %H:%M")}') 
        
    
    except:
        st.markdown("## Oops We dont have that currency!")

    try:
        
        if amount != 0.0:
            total = convert_to + " "+ "{:,.2f}".format(converted)
            
            html_total = f"""
            <style>
            p.a {{
            font: bold {30}px Courier;
            text-align: center;
            }}
            </style>
            <p class="a">{total}</p>
            """
            st.write(" ")
            st.markdown(html_total, unsafe_allow_html=True)
    except:
        " "        
#button
if st.button("Convert"):
    xchange_fnc(base_currency, convert_to)



