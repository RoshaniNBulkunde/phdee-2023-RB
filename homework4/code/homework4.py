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
FishBycatchLong2 = FishBycatchLongR.drop(['firmsize', 'salmon', 'shrimp'], axis = 1)

## Create a subsample of the data that have observations in December 2017 and January 2018 only
monthvalues = [12, 13]
FishBycatchLong2 = FishBycatchLong2[FishBycatchLong2.month.isin(monthvalues) == True]
## Count the number of observations
t0p0 = sum((FishBycatchLong2.treated ==0) & (FishBycatchLong2.month <13))
t0p1 = sum((FishBycatchLong2.treated ==0) & (FishBycatchLong2.month >12))
t1p0 = sum((FishBycatchLong2.treated ==1) & (FishBycatchLong2.month <13))
t1p1 = sum((FishBycatchLong2.treated ==1) & (FishBycatchLong2.month >12))
n=100

## Sum of Bycatch by treatment and pre-post status 
yi_t0p0 = FishBycatchLong2.loc[(FishBycatchLongR['treated'] == 0) & (FishBycatchLong2['month'] <13), 'bycatch'].sum()
yi_t0p1 = FishBycatchLong2.loc[(FishBycatchLongR['treated'] == 0) & (FishBycatchLong2['month'] >12), 'bycatch'].sum()
yi_t1p0 = FishBycatchLong2.loc[(FishBycatchLongR['treated'] == 1) & (FishBycatchLong2['month'] <13), 'bycatch'].sum()
yi_t1p1 = FishBycatchLong2.loc[(FishBycatchLongR['treated'] == 1) & (FishBycatchLong2['month'] >12), 'bycatch'].sum()

## Calculate expected values
Eyi_t0p0 = (t0p0/n) * yi_t0p0
Eyi_t0p1 = (t0p1/n) * yi_t0p1
Eyi_t1p0 = (t1p0/n) * yi_t1p0
Eyi_t1p1 = (t1p1/n) * yi_t1p1

## Difference-in-difference Estimate
did = (Eyi_t1p1 - Eyi_t1p0) - (Eyi_t0p1 - Eyi_t0p0)

############################################################################################################

#*************  Question 3 **************************************

# Part a --------------------------------------------------------------

## Create the subset of the data needed only for this part of the question
FishBycatchLongR3 = FishBycatchLongR.drop(['firmsize', 'salmon', 'shrimp'], axis = 1)

## Create a subsample of the data that have observations in December 2017 and January 2018 only
monthvalues = [12, 13]
FishBycatchLongR3a = FishBycatchLongR3[FishBycatchLongR3.month.isin(monthvalues) == True]

## Create new variables that indicate the pre-post situation
FishBycatchLongR3a['pre'] = FishBycatchLongR3a.apply(lambda row: 13 - row.month, axis = 1) ## Pre=1 if December 2017
FishBycatchLongR3a['post'] = FishBycatchLongR3a.apply(lambda row: row.month - 12, axis = 1) ## Post=1 if January 2018

## Now create the variables needed for our regression
FishBycatchLongR3a['posttreat'] = FishBycatchLongR3a.apply(lambda row: row.post*row.treated, axis = 1)
#FishBycatchLongR3a = FishBycatchLongR3a.drop(['post'], axis = 1)
constant3a = pd.DataFrame(np.ones((100))) # Vector of ones for the constant

## Dataframes
treatment = pd.DataFrame(FishBycatchLongR3a['treated']).reset_index().drop(['index'], axis = 1)
pre2017_intercept = pd.DataFrame(FishBycatchLongR3a['pre']).reset_index().drop(['index'], axis = 1)
posttreatment = pd.DataFrame(FishBycatchLongR3a['posttreat']).reset_index().drop(['index'], axis = 1)

## OLS setup
xvar = pd.concat([constant3a, pre2017_intercept, treatment, posttreatment], axis = 1) # X matrix
xvar.columns =['constant3a', 'pre2017_intercept', 'treatment', 'posttreatment'] # naming columns
xvar = xvar.to_numpy() #convert to array

bycatch = pd.DataFrame(FishBycatchLongR3a['bycatch']).reset_index().drop(['index'], axis = 1)
bycatch = bycatch.to_numpy() #convert to array to use in OLS

# DID Estimates
ols3a = sm.OLS(bycatch, xvar)
betaols3afit = ols3a.fit()
print(betaols3afit.summary())
betaols3a = betaols3afit.params




#*************  Question 3 **************************************

# Part b --------------------------------------------------------------

## Create the subset of the data needed only for this part of the question
FishBycatchLong3b = FishBycatchLongR.drop(['firmsize', 'salmon', 'shrimp', 'firm'], axis = 1)

## Create new variables that indicate the pre-post situation
def post(value):
    if value < 13:  ## Post=0 if 2017
        return 0
    elif 13 <= value: ## Post=1 if 2018
        return 1
 
FishBycatchLong3b['post'] = FishBycatchLong3b['month'].map(post)

## Now create the variables needed for our regression
FishBycatchLong3b['posttreat'] = FishBycatchLong3b.apply(lambda row: row.post*row.treated, axis = 1)   # posttreat=1 if treated=1 and post=1

## Set up a few things we will need
bycatch = FishBycatchLong3b['bycatch'].to_numpy()
nobs3b = bycatch.shape
constant = pd.DataFrame(np.ones(1200)) # Vector of ones for the constant
FishBycatchLong3b = FishBycatchLong3b[["post", "treated", "posttreat", "month", "bycatch"]]
Xvar3b = FishBycatchLong3b.drop(['month', 'bycatch'] ,axis = 1) #Create Xvar matrix
Xvar3b = pd.concat([constant,Xvar3b], axis = 1) # Add the constant
Xvar3b.columns =['constant', 'post', 'treated', 'posttreat'] # naming columns
Xvar3b = Xvar3b.to_numpy() #convert to array


# DID Estimates
ols3b = sm.OLS(bycatch, Xvar3b)
betaols3bfit = ols3b.fit()
print(betaols3bfit.summary())
betaols3b = betaols3bfit.params

#*************  Question 3 **************************************

# Part c --------------------------------------------------------------

## Create the subset of the data needed only for this part of the question
FishBycatchLong3c = FishBycatchLongR.drop(['firm'], axis = 1)

## Create new variables that indicate the pre-post situation
def post(value):
    if value < 13:  ## Post=0 if 2017
        return 0
    elif 13 <= value: ## Post=1 if 2018
        return 1
 
FishBycatchLong3c['post'] = FishBycatchLong3c['month'].map(post)

## Now create the variables needed for our regression
FishBycatchLong3c['posttreat'] = FishBycatchLong3c.apply(lambda row: row.post*row.treated, axis = 1)   # posttreat=1 if treated=1 and post=1

## Set up a few things we will need
bycatch = FishBycatchLong3c['bycatch'].to_numpy()
nobs3c = bycatch.shape
constant = pd.DataFrame(np.ones(1200)) # Vector of ones for the constant
FishBycatchLong3c = FishBycatchLong3c[["post", "treated", "posttreat", "month", "bycatch", "firmsize", "shrimp", "salmon"]] # reordering columns
Xvar3c = FishBycatchLong3c.drop(['month', 'bycatch'] ,axis = 1) #Create Xvar matrix
Xvar3c = pd.concat([constant,Xvar3c], axis = 1) # Add the constant
Xvar3c = Xvar3c.to_numpy() #convert to array


# DID Estimates
ols3c = sm.OLS(bycatch, Xvar3c)
betaols3cfit = ols3c.fit()
print(betaols3cfit.summary())
betaols3c = betaols3cfit.params

