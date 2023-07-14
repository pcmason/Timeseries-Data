#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 18:07:55 2023

Code using pandas_datareader to fetch time series data from multiple sources. 

@author: paulmason
"""
'''
STOCK DATA
'''

from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import yfinance as yf
from datetime import datetime, date

yf.pdr_override()

#List of companies to get stock data on 
companies = ['AAPL', 'MSFT', 'GE']
shares_multiple_df = pdr.get_data_yahoo(companies, start = datetime(2022, 1, 1), end = datetime(2022, 12, 31))
print(shares_multiple_df)

def plot_timeseries_df(df, attrib, ticker_loc = 1, title = "Timeseries", legend = ''):
    #General routine for plotting time series data
    fig = plt.figure(figsize = (15, 7))
    plt.plot(df[attrib], 'o-')
    _ = plt.xticks(rotation = 90)
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(ticker_loc))
    plt.title(title)
    plt.gca().legend(legend)
    plt.show()
    
plot_timeseries_df(shares_multiple_df.loc["2022-03-01" : "2022-07-31"], "Close",
                   ticker_loc = 3, title = "Close Price", legend = companies)

'''
FRED DATA
'''

import pandas_datareader as pdr

#Now get data from FRED and output data
fred_df = pdr.DataReader(['CPIAUCSL', 'CPILFESL'], 'fred', "2010-01-01", "2022-12-31")
print(fred_df)

#Show in plot data from 2020 - 2022
fig = plt.figure(figsize = (15, 7))
plt.plot(fred_df.loc["2020": ], 'o-')
plt.xticks(rotation = 90)
plt.legend(fred_df.columns)
plt.title('Consumer Price Index')
plt.show()

'''
WORLD BANK DATA
'''
import pandas_datareader.wb as wb
import pandas as pd

#Get list of 2-letter country code excluding aggregates
countries = wb.get_countries()
countries = list(countries[countries.region != "Aggregates"]["iso2c"])

#Read countries total pop data in year 2022
population_df = wb.download(indicator = "SP.POP.TOTL", country = countries, start = 2022, end = 2022)

#Sort by pop then take top 25 countries and make index as a column
population_df = (population_df.dropna()
                              .sort_values("SP.POP.TOTL")
                              .iloc[-25:]
                              .reset_index())

#Plot the pop in millions
fig = plt.figure(figsize = (15, 7))
plt.bar(population_df["country"], population_df["SP.POP.TOTL"] / 1e6)
plt.xticks(rotation = 90)
plt.ylabel("Million Population")
plt.title("Population")
plt.show()
