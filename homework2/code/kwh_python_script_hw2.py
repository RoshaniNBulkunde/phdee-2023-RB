# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 05:45:27 2023

@author: roshani bulkunde
"""
# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages - you may need to type "conda install numpy" the first time you use a package, for example.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ttest_ind_from_stats

# Set working directories and seed

## The "outputpath" is where I will export my outputs
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework2\output'

#Create a table that displays each variable’s sample mean, sample standard deviation, and p-values for the two-way t-test between
#treatment and control group means

## Import kwh.csv data
kwhData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework2\\kwh.csv')

## Just to view summary statistics
print(kwhData.describe())

# Summary for Control group

## Generate means for control group
meanControlEle = kwhData[kwhData["retrofit"]==0]["electricity"].mean()
meanControlSqft = kwhData[kwhData["retrofit"]==0]["sqft"].mean()
meanControlTemp = kwhData[kwhData["retrofit"]==0]["temp"].mean()

meansControl= pd.Series([meanControlEle, meanControlSqft, meanControlTemp]) ##Create a series for means of variable for control group


## Generate standard deviation for control group
stdControlEle = kwhData[kwhData["retrofit"]==0]["electricity"].std()
stdControlSqft = kwhData[kwhData["retrofit"]==0]["sqft"].std()
stdControlTemp = kwhData[kwhData["retrofit"]==0]["temp"].std()

stdvControl= pd.Series([stdControlEle, stdControlSqft, stdControlTemp]) ##Create a series for standard deviation of variable for control group

## Generate number of observation for control group
obControl = kwhData[kwhData["retrofit"]==0].count().min()


# Summary for Treatment group

## Generate means for control group
meanTreatEle = kwhData[kwhData["retrofit"]==1]["electricity"].mean()
meanTreatSqft = kwhData[kwhData["retrofit"]==1]["sqft"].mean()
meanTreatTemp = kwhData[kwhData["retrofit"]==1]["temp"].mean()

meansTreat = pd.Series([meanTreatEle, meanTreatSqft, meanTreatTemp]) ##Create a series for means of variable for treatment group


## Generate standard deviation for control group
stdTreatEle = kwhData[kwhData["retrofit"]==1]["electricity"].std()
stdTreatSqft = kwhData[kwhData["retrofit"]==1]["sqft"].std()
stdTreatTemp = kwhData[kwhData["retrofit"]==1]["temp"].std()

stdvTreat= pd.Series([stdTreatEle, stdTreatSqft, stdTreatTemp]) ##Create a series for standard deviation of variable for treatment group

## Generate number of observation for control group
obTreat = kwhData[kwhData["retrofit"]==1].count().min()

# T Test

#Create Control and Treatment datasets
control = kwhData[kwhData['retrofit']==0]
treat = kwhData[kwhData['retrofit']==1]

#Perform ttest
electricity_test = ttest_ind(treat['electricity'], control['electricity'])
electricity_test =pd.DataFrame(electricity_test)

sqft_test = ttest_ind(treat['sqft'], control['sqft'])
sqft_test = pd.DataFrame(sqft_test)

temp_test = ttest_ind(treat['temp'], control['temp'])
temp_test = pd.DataFrame(temp_test)

obs = kwhData.count().min()

## Set the row and column names
rownames = pd.concat([pd.Series(['Electricity (kWh)','Home (sqft)','Temperature', 'Observations']),pd.Series([' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
colnames = [('Mean','(s.d.)')] # Two rows of column names
coldiff = [('Diff','(p value)')]

## Format means and std devs to display to two decimal places
meansControl = meansControl.map('{:.2f}'.format)
stdvControl = stdvControl.map('({:.2f})'.format)
meansTreat = meansTreat.map('{:.2f}'.format)
stdvTreat = stdvTreat.map('({:.2f})'.format)

## Align std deviations under means and add observations
col0 = pd.concat([meansControl, stdvControl],axis = 1).stack()
col0 = pd.concat([col0, pd.Series(obControl)], axis=0)

col1 = pd.concat([meansTreat, stdvTreat],axis = 1).stack()
col1 = pd.concat([col1, pd.Series(obTreat)], axis=0)
#col1 = pd.concat([meansTreat, stdvTreat, pd.Series(obTreat)],axis = 1).stack()

col2 = pd.concat([electricity_test, sqft_test, temp_test, pd.Series(obs)],axis = 0)



## Add column and row labels.  Convert to dataframe (helps when you export it)
col0 = pd.DataFrame(col0)
col0.index = rownames
col0.columns = pd.MultiIndex.from_tuples(colnames)

col1 = pd.DataFrame(col1)
col1.index = rownames
col1.columns = pd.MultiIndex.from_tuples(colnames)

col2 = pd.DataFrame(col2)
col2.index = rownames
col2.columns = pd.MultiIndex.from_tuples(coldiff)

summary = pd.concat([col0, col1, col2], axis = 1)

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

summary.to_latex('pythonsummary.tex')



##Converting to wide data frame
kwhdata_wide = kwhData.pivot(columns='retrofit', values='electricity')

## Plot kernel density
kwhdata_wide.plot.density(figsize = (7, 7), linewidth = 4) 
plt.xlabel("Electricity Distribution (kWh)")
plt.savefig('python_kwh_hist.pdf',format='pdf') # I suggest saving to .pdf for highest quality
plt.show()
