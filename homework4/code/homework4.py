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
nobs3a = bycatch.shape


#********************** DID Estimates Without cluster-robust standard errors**************************#
betaols3afit = sm.OLS(bycatch, xvar).fit()
print(betaols3afit.summary())
betaols3a = betaols3afit.params
stderrols3a = betaols3afit.bse ## Extract the standard errors

## Build output table
### Reorder output (I probably should figure out a way to do this all at once)
order3a = np.array([1,2,3,0])
betaols3a = betaols3a[order3a]
stderrols3a = stderrols3a[order3a]

### Row and column names
rownames3a = pd.concat([pd.Series(['T=2017 intercept', 'Treatment', 'Treatment*Post', 'Constant', 'Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack()
colnames3a = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3a = pd.Series(np.round(stderrols3a,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3a = pd.Series(np.append(np.round(betaols3a,2), nobs3a))
betaols3a = betaols3a.drop(index=5)
stderrols3a = pd.Series((np.round(stderrols3a,2)))

### Stack estimates over Standard Errors
col3a = pd.concat([betaols3a,stderrols3a],axis = 1).stack()
col3a1 = col3a

### Output
col3a.index = rownames3a
col3a.columns = colnames3a

print(col3a)

col3a.to_latex('DID3a_python.tex')


#********************** DID Estimates With cluster-robust standard errors**************************#

ols3aC = sm.OLS(bycatch, xvar) #Fit in the model
betaols3afitC = ols3aC.fit(cov_type = 'cluster', cov_kwds={'groups': FishBycatchLongR3a['firm']})
print(betaols3afitC.summary())
betaols3aC = betaols3afitC.params
stderrols3aC = betaols3afitC.bse

## Build output table
### Reorder output (I probably should figure out a way to do this all at once)
order3a = np.array([1,2,3,0])
betaols3aC = betaols3aC[order3a]
stderrols3aC = stderrols3aC[order3a]

### Row and column names
rownames3a = pd.concat([pd.Series(['T=2017 intercept', 'Treatment', 'Treatment*Post', 'Constant', 'Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack()
colnames3a = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3aC = pd.Series(np.round(stderrols3aC,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3aC = pd.Series(np.append(np.round(betaols3aC,2), nobs3a))
betaols3aC = betaols3aC.drop(index=5)
stderrols3aC = pd.Series((np.round(stderrols3aC,2)))

### Stack estimates over Standard Errors
col3aC = pd.concat([betaols3aC,stderrols3aC],axis = 1).stack()

### Output
col3aC.index = rownames3a
col3aC.columns = colnames3a

print(col3aC)

col3aC.to_latex('DID3a_clusterstd_python.tex')

#####################################################################################################################################
#*************  Question 3 **************************************

# Part b --------------------------------------------------------------

## Create the subset of the data needed only for this part of the question
FishBycatchLong3b = FishBycatchLongR.drop(['firmsize', 'salmon', 'shrimp'], axis = 1)

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
bycatch = FishBycatchLong3b['bycatch'].to_numpy() # y variable
nobs3b = bycatch.shape # Number of observations

FishBycatchLong3b = FishBycatchLong3b[["firm", "month", "treated", "posttreat",  "post", "bycatch"]] #Rearranging the columns
Xvar3b = FishBycatchLong3b.drop(['post', 'bycatch'] ,axis = 1) #Create Xvar matrix

Xvar3b = Xvar3b.to_numpy() #convert to array


#******************************DID Estimates Without cluster-robust standard errors*********************#
betaols3bfit = sm.OLS(bycatch, Xvar3b).fit()
print(betaols3bfit.summary())
betaols3b = betaols3bfit.params
stderrols3b = betaols3bfit.bse ## Extract the standard errors

## Build output table

### Row and column names
rownames3b = pd.concat([pd.Series(['Firm', 'Month', 'Treatment', 'Treatment*Post', 'Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack()
colnames3b = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3b = pd.Series(np.round(stderrols3b,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3b = pd.Series(np.append(np.round(betaols3b,2), nobs3b))
stderrols3b = pd.Series((np.round(stderrols3b,2)))

### Stack estimates over Standard Errors
col3b = pd.concat([betaols3b,stderrols3b],axis = 1).stack()
col3b1 =col3b

### Output
col3b.index = rownames3b
col3b.columns = colnames3b

print(col3b)

col3b.to_latex('DID3b_python.tex')

#******************************DID Estimates With cluster-robust standard errors*********************#
ols3bC = sm.OLS(bycatch, Xvar3b)
betaols3bfitC = ols3bC.fit(cov_type = 'cluster', cov_kwds={'groups': FishBycatchLong3b['firm']}) 
print(betaols3bfitC.summary())
betaols3bC = betaols3bfitC.params
stderrols3bC = betaols3bfitC.bse ## Extract the standard errors

## Build output table

### Row and column names
rownames3b = pd.concat([pd.Series(['Firm', 'Month', 'Treatment', 'Treatment*Post', 'Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack()
colnames3b = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3bC = pd.Series(np.round(stderrols3bC,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3bC = pd.Series(np.append(np.round(betaols3bC,2), nobs3b))
stderrols3bC = pd.Series((np.round(stderrols3bC,2)))

### Stack estimates over Standard Errors
col3bC = pd.concat([betaols3bC,stderrols3bC],axis = 1).stack()

### Output
col3bC.index = rownames3b
col3bC.columns = colnames3b

print(col3bC)

col3bC.to_latex('DID3b_clusterstd_python.tex')
####################################################################################################################

#*************  Question 3 **************************************

# Part c --------------------------------------------------------------

## Create the subset of the data needed only for this part of the question
FishBycatchLong3c = FishBycatchLongR

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
bycatch = FishBycatchLong3c['bycatch'].to_numpy() # Y variable
nobs3c = bycatch.shape

FishBycatchLong3c = FishBycatchLong3c[["firm", "month", "treated", "posttreat", "firmsize", "shrimp", "salmon", "bycatch", "post"]] # reordering columns
Xvar3c = FishBycatchLong3c.drop(['post', 'bycatch'] ,axis = 1) #Create Xvar matrix
Xvar3c = Xvar3c.to_numpy() #convert to array


#****************** DID Estimates without cluster-robust standard errors *********************#
betaols3cfit = sm.OLS(bycatch, Xvar3c).fit()
print(betaols3cfit.summary())
betaols3c = betaols3cfit.params ## Extract the coeffcients
stderrols3c = betaols3cfit.bse ## Extract the standard errors

## Build output table

### Row and column names
rownames4 = pd.concat([pd.Series(['Firm', 'Month', 'Treatment', 'Treatment*Post', 'Firmsize', 'Shrimp','Salmon', 'Observations']),pd.Series([' ',' ',' ',' ',' ',' ',' '])],axis = 1).stack()
colnames4 = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3c = pd.Series(np.round(stderrols3c,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3c = pd.Series(np.append(np.round(betaols3c,2), nobs3c))
stderrols3c = pd.Series((np.round(stderrols3c,2)))

### Stack estimates over Standard Errors
col3c = pd.concat([betaols3c,stderrols3c],axis = 1).stack()

### Output
col3c.index = rownames4
col3c.columns = colnames4

print(col3c)

col3c.to_latex('DID3c_python.tex')

#****************** DID Estimates with cluster-robust standard errors *********************#
ols3cfit = sm.OLS(bycatch, Xvar3c)
betaols3cfitC= ols3cfit.fit(cov_type = 'cluster', cov_kwds={'groups': FishBycatchLong3c['firm']})
print(betaols3cfitC.summary())
betaols3cC = betaols3cfitC.params ## Extract the coeffcients
stderrols3cC = betaols3cfitC.bse ## Extract the standard errors

## Build output table

### Row and column names
rownames4 = pd.concat([pd.Series(['Firm', 'Month', 'Treatment', 'Treatment*Post', 'Firmsize', 'Shrimp','Salmon', 'Observations']),pd.Series([' ',' ',' ',' ',' ',' ',' '])],axis = 1).stack()
colnames4 = pd.Series(['Coefficients'])

### Format Standard Errors
stderrols3cC = pd.Series(np.round(stderrols3cC,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
betaols3cC = pd.Series(np.append(np.round(betaols3cC,2), nobs3c))
stderrols3cC = pd.Series((np.round(stderrols3cC,2)))

### Stack estimates over Standard Errors
col3cC = pd.concat([betaols3cC,stderrols3cC],axis = 1).stack()

### Output
col3cC.index = rownames4
col3cC.columns = colnames4

print(col3cC)

col3cC.to_latex('DID3c_cluster_python.tex')

###############################################################################################

#####***************** Question 3--- part d ************************************************#
col3a1.loc[4, 1] = ' '
col3a1.loc[5, 0] = ' '
col3a1.loc[5, 1] = ' '
col3a1.loc[6, 0] = ' '
col3a1.loc[6, 1] = ' '
col3a1.loc[7, 0] = ' '

### Row and column names
rownames5 = pd.concat([pd.Series(['T=2017 intercept', 'Firm', 'Month', 'Treatment', 'Treatment*Post', 'Firmsize', 'Shrimp','Salmon','constant', 'Observations']),pd.Series([' ',' ',' ',' ',' ',' ',' ',' ', ' '])],axis = 1).stack()
colnames5 = pd.Series(['Coefficients'])

rownames5=pd.DataFrame(rownames5)

col3cC1 = pd.DataFrame(col3cC)
col3bC1 = pd.DataFrame(col3bC)
#col3cC.index = rownames4
#col3cC.columns = pd.MultiIndex.from_tuples(colnames4)
#summary = pd.MultiIndex.from_frame([rownames5, col3cC])

#xx=pd.concat((col3bC1,col3cC1), ignore_index=True, join='inner', axis=1)
y=pd.merge(col3bC1,col3cC1, how='right', on=['index'], axis=1)