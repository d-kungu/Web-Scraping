
'''Data Extraction from https://api.openchargemap.io/v3/poi/ a API that store data
electric vehicles charging points.

- This script extracts all EV charging points in Great Britain
-Authorization key is required: see documentation

    Created by
** Diana Kung'u **
'''

#IMPORTS
from pandas import DataFrame, json_normalize, concat, merge
from requests import get
from numpy import where
from os import environ

# Create URL 
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
key = environ.get('OCM_KEY') #Authorization key stored as system variable
headers = {'User-Agent': ua} # User-Agent
query_dict = {'countrycode': 'GB', 'maxresults': 1000000, 'key': key, 
                    'opendata': 'true', 'compact':'true'  } #Parameters
base_url = 'https://api.openchargemap.io/v3/poi/'

# Connect to the API
response = get(base_url, params=query_dict, headers = headers)  
response.status_code
results = response.json()


# Extract required data
labels = ['UsageTypeID', 'AddressInfo', 'NumberOfPoints', 'connections']
conn_lsts = ['ConnectionTypeID', 'Amps', 'Voltage', 'PowerKW', 'LevelID']

all_results = []

for i in results:
    info = []
    connections = i['Connections']
    connection_info = [{key: d[key] for key in d.keys and conn_lsts} for d in connections]

    info = [i.get(label) for label in labels]
    info = info[:-1]
    info.append(connection_info)
    all_results.append(dict(zip(labels, info)))

# Create a dataframe will extracted data
df = DataFrame(all_results)


#CLEAN DATAFRAME
#Explode by connection field
df_exploded = df.explode('connections', ignore_index= True)

# Create Address fields from AddressInfo field
add_labels = ['ID', 'Town', 'Latitude', 'Longitude', 'StateOrProvince', 'Postcode', 'Title']
df_exploded['AddressInfo'] = df_exploded['AddressInfo'].apply(
                                lambda x: {key: x[key] for key in x.keys and add_labels})
df_address = json_normalize(df_exploded['AddressInfo'])
df_address['Address'] = df_address['Title'] + ' ' + df_address['Postcode']
df_address['Areacode'] = df_address['Postcode'].str.extract(r'(\w+\d+)')
df_address.drop(['Title'], axis = 1, inplace = True)

# Create connection fields from Connection field Dictionaries
df_connections = json_normalize(df_exploded['connections'])

#Concatinate the address and connections dataframe
df2 = concat([df_exploded.drop(['connections', 'AddressInfo'], axis=1), 
                df_connections, df_address], axis= 1)

#Clean rows where Latitude and Longitude entries are interchanged
arr = where(df2['Longitude'] > df2['Latitude'], [df2['Longitude'],df2['Latitude']], 
            [df2['Latitude'], df2['Longitude']] )
df2['Latitude'] = arr[0]
df2['Longitude'] = arr[1]

#Load connection types reference data
ref = get("https://raw.githubusercontent.com/openchargemap/ocm-data/master/reference.json")
txt = ref.json()['ConnectionTypes']

#Create a Connection Type reference dataframe
reference_df = (DataFrame(txt)).iloc[:, :2]
reference_df.ID = reference_df['ID'].astype(float)

#Merge 
df2.rename(columns={"ID": 'LOC_ID'}, inplace= True)
df2 = merge(df2, reference_df, how = 'left', left_on = 'ConnectionTypeID', right_on = 'ID')

# OUTPUT
df2.to_csv(r'.\Data\EV_Charging_Points_GB.csv', index= False)
print ('end')


