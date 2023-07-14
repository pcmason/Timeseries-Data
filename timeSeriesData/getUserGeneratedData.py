#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 19:20:45 2023

Generate an autoregressive time series dataset using numpy

@author: paulmason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Predefined parameters
#Order of the AR(n) data
ar_n = 3
#Coefficients b_3, b_2, b_1
ar_coeff = [0.7, -0.3, -0.1]
#Noise added to the AR(n) data
noise_level = 0.1
#Number of data points to generate
length = 200

#Random initial values
ar_data = list(np.random.randn(ar_n))

#Generate the rest of the values
for i in range(length - ar_n):
    next_val = (np.array(ar_coeff) @ np.array(ar_data[-3:])) + np.random.randn() * noise_level
    ar_data.append(next_val)
    
#Convert data into a pandas DataFrame
synthetic = pd.DataFrame({"AR(3)": ar_data})
synthetic.index = pd.date_range(start = "2022-07-01", periods = len(ar_data), freq = "D")

#Plot the time series
fig = plt.figure(figsize = (12, 5))
plt.plot(synthetic.index, synthetic)
plt.xticks(rotation = 90)
plt.title("AR(3) Time Series")
plt.show()