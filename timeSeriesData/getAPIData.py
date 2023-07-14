#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 19:08:29 2023

Use the World Bank's API to create a bar graph for the 25 most populous countries in the world.

@author: paulmason
"""

import pandas as pd
import matplotlib.pyplot as plt
import requests

#Create query URL for list of countries
url = "http://api.worldbank.org/v2/country/all?format=json&per_page=500"
response = requests.get(url)
#Expect status code 200 for correct query
print(response.status_code)
#Get the response in JSON
header, data = response.json()
print(header)
#Collect list of 3-letter country code excluding aggregates
countries = [item["id"]
             for item in data
             if item["region"]["value"] != "Aggregates"]
print(countries)

#Create query URL for total pop from all countries in 2022
arguments = {
    "country": "all",
    "indicator": "SP.POP.TOTL",
    "date": 2022,
    "format": "json"    
}
url = "http://api.worldbank.org/v2/country/{country}/" \
      "indicator/{indicator}?date={date}&format={format}&per_page=500"
query_population = url.format(**arguments)
response = requests.get(query_population)
print(response.status_code)
#Get response in JSON
header, population_data = response.json()
print(header)

#Filter for countries not aggregates
population = []
for item in population_data:
    if item["countryiso3code"] in countries:
        name = item["country"]["value"]
        population.append({"country": name, "population": item["value"]})
        
#Create DataFrame for sorting and filtering
population = pd.DataFrame.from_dict(population)
population = population.dropna().sort_values("population").iloc[-25: ]
#Plot bar chart
fig = plt.figure(figsize = (15, 7))
plt.bar(population["country"], population["population"] / 1e6)
plt.xticks(rotation = 90)
plt.ylabel("Million Population")
plt.title("Population")
plt.show()