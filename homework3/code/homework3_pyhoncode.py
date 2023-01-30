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

outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework3\output'

## Import kwh.csv data
kwhData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework2\\kwh.csv')

# Question 1 (e)--------------------------------------------------------------

# Create the log variables in the KWH data itself
kwhData['ln_electricity'] =np.log(kwhData['electricity'])
kwhData['ln_sqft'] =np.log(kwhData['sqft'])
kwhData['ln_temp'] =np.log(kwhData['temp'])

# Set the numoy matrices for OLS
ln_electricity_array = kwhData['ln_electricity'].to_numpy() # Create an array of outcome variable
nobsa, = ln_electricity_array.shape # Numner of observations in Outcome variable
constant = np.ones((nobsa,1)) # Vector of ones for the constant
Xvar = kwhData[['ln_electricity', 'electricity', 'sqft', 'temp', 'ln_sqft', 'retrofit', 'ln_temp']] #Reordering th columns 
Xvar = Xvar.drop(['ln_electricity', 'electricity', 'sqft', 'temp'] ,axis = 1).to_numpy() #Create Xvar matrix
Xvar = np.concatenate([constant,Xvar],axis = 1) #Add the constant


## Simply call the statsmodels function.  Now there is an (arguably) easier way to do this using R-style syntax with an equation.
ols = sm.OLS(ln_electricity_array,Xvar).fit()
betaols = ols.params # The coeffcient estimates
nobsc = ols.nobs

## Calculate Avearage marginal effect

### Marginal effect of constant
margeff_constant_mean=0

### Average marginal effect of sqft
eta_sqft = betaols[1]
margeff_sqft = (eta_sqft * kwhData['electricity'])/kwhData['sqft']
margeff_sqft_mean = margeff_sqft.mean()

### Average marginal effect of retrofit
delta = (math.e)**betaols[2] # log of delta is coefficient of retrofit
margeff_retrofit = ((delta-1)/(delta**kwhData['retrofit']))*kwhData['electricity']
margeff_retrofit_mean = margeff_retrofit.mean()

### Average marginal effect of temperature
eta_temp = betaols[3]
margeff_temp = (eta_temp * kwhData['electricity'])/kwhData['temp']
margeff_temp_mean = margeff_temp.mean()

#Array of average marginal effect
average_margeff = pd.Series([margeff_constant_mean, margeff_sqft_mean, margeff_retrofit_mean, margeff_temp_mean])


## Output table without bootstapping
coefftable = pd.DataFrame((np.append(betaols,nobsa)),
                            columns=['Coefficient Estimates'], 
                            index = ['Constant', 'Sqft of home', 'Retrofit', 'Temperature','Observations'])


margefftable = pd.DataFrame((np.append(average_margeff,nobsa)),
                            columns=['Average Marginal Effect'], 
                            index = ['Constant', 'Sqft of home', 'Retrofit', 'Temperature','Observations'])

## Output table 1 without bootstrapping
outputtable1=pd.concat([coefftable, margefftable], axis=1, join='inner')

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

outputtable1.style.to_latex('outputtable1.tex')

#===================  Bootstrapping ================================#

# Fit a linear regression model to the data ----------------------------------
## Using statsmodels
ols = sm.OLS(ln_electricity_array,Xvar).fit()
betaols = ols.params # Save estimated parameters
params, = np.shape(betaols) # save number of estimated parameters
nobs3 = int(ols.nobs)


##---- Calculate and save average marginal effect estimate 
### Marginal effect of constant
margeff_constant_mean1=0

### Average marginal effect of sqft
eta_sqft = betaols[1]
margeff_sqft = (eta_sqft * kwhData['electricity'])/kwhData['sqft']
margeff_sqft_mean1 = margeff_sqft.mean()

### Average marginal effect of retrofit
delta = (math.e)**betaols[2] # log of delta is coefficient of retrofit
margeff_retrofit = ((delta-1)/(delta**kwhData['retrofit']))*kwhData['electricity']
margeff_retrofit_mean1 = margeff_retrofit.mean()

### Average marginal effect of temperature
eta_temp = betaols[3]
margeff_temp = (eta_temp * kwhData['electricity'])/kwhData['temp']
margeff_temp_mean1 = margeff_temp.mean()

#Array of average marginal effect
average_margeff = pd.Series([margeff_constant_mean1, margeff_sqft_mean1, margeff_retrofit_mean1, margeff_temp_mean1]) #save average marginal effect estimate 

# Bootstrap by hand and get confidence intervals -----------------------------

## Note that each bootstrap replication should perform both the regression and the second stage calculation of the marginal effect.
## Set values and initialize arrays to output to
breps = 1000 # number of bootstrap replications
olsbetablist = np.zeros((breps,params))

## Get an index of the data we will sample by sampling with replacement
bidx = np.random.choice(nobs3,(nobs3,breps)) # Generates random numbers on the interval [0,nobs3] and produces a nobs3 x breps sized array

## Create an empty array to store average marginal effect estimates while bootstrapping
margeff_sqft_mean = []
margeff_sqft_mean = [0 for i in range(1000)]

margeff_retrofit_mean = []
margeff_retrofit_mean = [0 for i in range(1000)]

margeff_temp_mean = []
margeff_temp_mean = [0 for i in range(1000)]

#-------For loop to bootstrap replication to perform both the regression and the second stage calculation of the marginal effect.
## Sample with replacement to get the size of the sample on each iteration
for r in range(breps):
### Sample the data
    kwhDataB = kwhData.iloc[bidx[:,r]]
    ## Data to perform ols
    kwhDataB2 = kwhDataB.drop(['electricity', 'sqft', 'temp'] ,axis = 1)
    kwhDataB2 = kwhDataB[['ln_electricity', 'ln_sqft', 'retrofit', 'ln_temp']] #Reordering th columns
    ### Perform the estimation
    olsB = sm.OLS(kwhDataB2['ln_electricity'],sm.add_constant(kwhDataB2.drop('ln_electricity',axis = 1))).fit()
    ### Output the result
    olsbetablist[r,:] = olsB.params
    ## Calculate the average estimates

    ### Average marginal effect of sqft
    eta_sqft = olsbetablist[r,1]
    margeff_sqft = (eta_sqft * kwhDataB['electricity'])/kwhDataB['sqft']
    margeff_sqft_mean[r] = margeff_sqft.mean()

    ### Average marginal effect of retrofit
    delta = (math.e)**olsbetablist[r,2] # log of delta is coefficient of retrofit
    margeff_retrofit = ((delta-1)/(delta**kwhDataB['retrofit']))*kwhDataB['electricity']
    margeff_retrofit_mean[r] = margeff_retrofit.mean()

    ### Average marginal effect of temperature
    eta_temp = olsbetablist[r,3]
    margeff_temp = (eta_temp * kwhDataB['electricity'])/kwhDataB['temp']
    margeff_temp_mean[r]= margeff_temp.mean()

#----------End of For loop  
    
#--------For Coeffcient of estimates to calculate confidence interval
## Extract 2.5th and 97.5th percentile
lb = np.percentile(olsbetablist,2.5,axis = 0,interpolation = 'lower')
ub = np.percentile(olsbetablist,97.5,axis = 0,interpolation = 'higher')

# Regression output table with CIs
## Format estimates and confidence intervals
betaols = np.round(betaols,2)

lbP = pd.Series(np.round(lb,2)) # Round to two decimal places and get a Pandas Series version
ubP = pd.Series(np.round(ub,2))
ci = '(' + lbP.map(str) + ', ' + ubP.map(str) + ')'

## Get output in order
order = [1,2,3,0]
outputa = pd.DataFrame(np.column_stack([betaols,ci])).reindex(order)

## Row and column names
rownames = pd.concat([pd.Series(['sqft of home','Retrofit','Temperature','Constant','Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for CIs
colnames = ['Estimates']

## Append CIs, # Observations, row and column names
outputa = pd.DataFrame(outputa.stack().append(pd.Series(nobs3)))
outputa.index = rownames
outputa.columns = colnames   
    
#-------For Marginal Avarage Effect to calculate confidence interval
margeff_sqft_mean = np.array(margeff_sqft_mean)  
margeff_sqft_mean = pd.DataFrame(margeff_sqft_mean) 

margeff_retrofit_mean = np.array(margeff_retrofit_mean)
margeff_retrofit_mean = pd.DataFrame(margeff_retrofit_mean)

margeff_temp_mean = np.array(margeff_temp_mean)
margeff_temp_mean = pd.DataFrame(margeff_temp_mean)

zeroes = [0]*1000
zeroes = np.array(zeroes)
zeroes = pd.DataFrame(zeroes)

#Get the estimates of avarage marginal effect
ame =pd.concat([zeroes, margeff_sqft_mean, margeff_retrofit_mean, margeff_temp_mean], axis=1 )
 
## Extract 2.5th and 97.5th percentile
lb_ame = np.percentile(ame,2.5,axis = 0,interpolation = 'lower')
ub_ame = np.percentile(ame,97.5,axis = 0,interpolation = 'higher')

# Regression output table with CIs
## Format estimates and confidence intervals
average_margeff = np.round(average_margeff,2)

lbP_ame = pd.Series(np.round(lb_ame,2)) # Round to two decimal places and get a Pandas Series version
ubP_ame = pd.Series(np.round(ub_ame,2))
ci_ame = '(' + lbP_ame.map(str) + ', ' + ubP_ame.map(str) + ')'

## Get output in order
order = [1,2,3,0]
outputb = pd.DataFrame(np.column_stack([average_margeff,ci_ame])).reindex(order)

## Row and column names
rownames1 = pd.concat([pd.Series(['sqft of home','Retrofit','Temperature','Constant','Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for CIs
colnames1 = ['Average Marginal Effect']

## Append CIs, # Observations, row and column names
outputb = pd.DataFrame(outputb.stack().append(pd.Series(nobs3)))
outputb.index = rownames1
outputb.columns = colnames1

estimates_output = pd.concat([outputa, outputb], axis = 1)

## Output directly to LaTeX
estimates_output.style.to_latex('estimates_output.tex')

########################################################################

#-------Question 1 (f)

#Graph the average marginal effects of outdoor temperature and square feet of the home with
##bands for their bootstrapped confidence intervals

## Create an array which contains marginal effect only for outdoor temperature and square feet of the home
ame_temp_sqft = np.array([margeff_sqft_mean1, margeff_temp_mean1])

# Create an array for lower bound CI 
myorder = [0, 2, 1, 3]
lbP_ame1 = [lbP_ame[i] for i in myorder]
lbP_ame1 = lbP_ame1[2:]
lbP_ame1 = np.array(lbP_ame1)

# Create an array for upper bound CI 
myorder = [0, 2, 1, 3]
ubP_ame1 = [ubP_ame[i] for i in myorder]
ubP_ame1 = ubP_ame1[2:]
ubP_ame1 = np.array(ubP_ame1)

# Plot regression output with error bars -------------------------------------
lowbar = np.array(ame_temp_sqft - lbP_ame1)
highbar = np.array(ubP_ame1 - ame_temp_sqft)
plt.errorbar(y = ame_temp_sqft, x = np.arange(2), yerr = [lowbar,highbar], fmt = 'o', capsize = 5)
plt.ylabel('Average marginal effects estimate')
plt.xticks(np.arange(2),['sqft of home', 'Temperature'])
plt.xlim((-0.5,1.5)) # Scales the figure more nicely
plt.axhline(linewidth=2, color='r')
plt.savefig('amebootstrappedCI.pdf',format='pdf')
plt.show()





