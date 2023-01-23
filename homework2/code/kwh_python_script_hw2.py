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

# Question 3
##Q 3A

kwhData['ones']=1 #Create a column of ones

##Rearrange the order of the variables
kwhdata1 = kwhData[['electricity', 'ones', 'sqft', 'retrofit', 'temp']]

#Create an X matrix (array) that contains covariates
X = kwhdata1[kwhdata1.columns[1:5]].to_numpy()
np.shape(X) #1000 rows and 4 columns
X_matrix = np.matrix(X) #convert array into matrix

#Create an Y matrix (array) as a vector
Y = kwhdata1[kwhdata1.columns[0]].to_numpy()
np.shape(Y) #Dimension of Y matrix is 1000*1
Y_matrix = np.matrix(Y)
Y_matrix = np.transpose(Y_matrix) #because we need 1000*1

## Now we need to do matrix multiplication
X_tran= np.transpose(X)

XX = X_tran*X_matrix  ## Xtranspose mupliply by X
XY =X_tran*Y_matrix   ## X transpose multiply by Y matrix

XX_inverse = np.linalg.inv(XX) ##Inverse of XX matrix 

#Beta gives the beta coefficient estimates
beta= XX_inverse * XY 
##This beta gives me the exact coeffient as STATA regress command

## Question 3B




## Question 3C
OLS_canned_routine = sm.OLS(Y, X).fit()  ##Y and X already defined in question 3A. Hence, Iam just using the model.

print(OLS_canned_routine.summary())




























#XX_trans = np.transpose(XX)
#X_tran= np.transpose(X)
#XY = np.multiply(Y, X_tran)
#XY_trans = np.transpose(XY)


#array_ones= np.ones(1000) 
#X_matrix =np.matrix(X)
#X_tran= np.transpose(X)


#y=np.array(kwhData)
# 