# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:28:19 2023
@author: roshani bulkunde
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages - you may need to type "conda install numpy" the first time you use a package, for example.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import math
import array as arr

# Set working directories and seed

datapath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework4'
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework4\output'

os.chdir(datapath) # To change the current working directory to specified path

## Import kwh.csv data
FishBycatchWide = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework4\\fishbycatch.csv')

## Convert panel data from wide form to long form
FishBycatchLong = pd.wide_to_long(FishBycatchWide, stubnames=['shrimp', 'salmon', 'bycatch'], i=['firm'], j='month')

## Reset the index 
FishBycatchLongR = FishBycatchLong.reset_index()

#*********************************************************************************************

#*************  Question 1 **************************************
## Create a treatment and control group
FishBycatchLongR1 = FishBycatchLongR[["month", "treated", "bycatch"]]

## Calculate theb average by treatemnet group and month
FishBycatchLongR1a = FishBycatchLongR1.groupby(['month', 'treated'])['bycatch'].mean()

FishBycatchLongR1a = FishBycatchLongR1a.reset_index() #Reset Index

## Plot the line graph
FishBycatchLongR1a.set_index('month').columns
FishBycatchLongR1a.groupby('treated')["bycatch"].plot(legend=True)

plt.title('Parallel Trend Graph') # adding title to the plot
plt.xlabel('Months') # adding Label to the x-axis
plt.ylabel('Bycatch') # adding Label to the y-axis 
plt.legend(["Not Treated", "Treated"]) # adding legend to the curve

os.chdir(outputpath) # Output directly to LaTeX folder
plt.savefig('paralleltrend.pdf',format='pdf') # I suggest saving to .pdf for highest quality  
############################################################################################################

#*************  Question 2 **************************************

## Count the number of observations
t0p0 = sum((FishBycatchLongR.treated ==0) & (FishBycatchLongR.month <13))
t0p1 = sum((FishBycatchLongR.treated ==0) & (FishBycatchLongR.month >12))
t1p0 = sum((FishBycatchLongR.treated ==1) & (FishBycatchLongR.month <13))
t1p1 = sum((FishBycatchLongR.treated ==1) & (FishBycatchLongR.month >12))
n=1200

## Sum of Bycatch by treatment and pre-post status 
yi_t0p0 = FishBycatchLongR.loc[(FishBycatchLongR['treated'] == 0) & (FishBycatchLongR['month'] <13), 'bycatch'].sum()
yi_t0p1 = FishBycatchLongR.loc[(FishBycatchLongR['treated'] == 0) & (FishBycatchLongR['month'] >12), 'bycatch'].sum()
yi_t1p0 = FishBycatchLongR.loc[(FishBycatchLongR['treated'] == 1) & (FishBycatchLongR['month'] <13), 'bycatch'].sum()
yi_t1p1 = FishBycatchLongR.loc[(FishBycatchLongR['treated'] == 1) & (FishBycatchLongR['month'] >12), 'bycatch'].sum()

## Calculate expected values
Eyi_t0p0 = (t0p0/n) * yi_t0p0
Eyi_t0p1 = (t0p1/n) * yi_t0p1
Eyi_t1p0 = (t1p0/n) * yi_t1p0
Eyi_t1p1 = (t1p1/n) * yi_t1p1

## Difference-in-difference Estimate
did = (Eyi_t1p1 - Eyi_t1p0) - (Eyi_t0p1 - Eyi_t0p0)

