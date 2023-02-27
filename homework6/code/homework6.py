# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 00:13:52 2023

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
from statsmodels.sandbox.regression import gmm
from linearmodels import IV2SLS, IVGMM, IVGMMCUE, IVLIML ##Need to run this first "pip install linearmodels"
from rdd import rdd #pip install rdd

# Set working directories and seed

datapath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework6'
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework6\output'

os.chdir(datapath) # To change the current working directory to specified path

## Import kwh.csv data
IvData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework6\\instrumentalvehicles.csv')


os.chdir(outputpath) # Output directly to LaTeX folder
##########################################################################################################################

#****************************** Question 2  ***************************#
threshold = 225 # Cutoff at 225 incehes
IvData['treatment'] = np.where(IvData['length'] >= threshold, 1, 0) #Treated if 



#Create a variable for length -cutoff
IvData['norm_length']= IvData['length']-threshold

plt.figure(figsize=(12, 8))
plt.scatter(IvData['norm_length'],IvData['mpg'], facecolors='none', edgecolors='r')
plt.axvline(x=0, color='b') #a line at the RD cutoff
plt.xlabel("Length")
plt.ylabel("Fuel efficiency (mpg")
plt.show()

plt.savefig('discontinuity_2.pdf',format='pdf') # I suggest saving to .pdf for highest quality 


##############################################################################################
#****************************** Question 3  ***************************#

IvData3 = IvData

## Fit into RDD model
model = rdd.rdd(IvData3, 'length', 'mpg', cut=threshold)
mod=model.fit()
print(mod.summary())

beta_FS3 = mod.params # Save the coeffcients from the first stage
stderr3 = mod.bse ## Extract the standard errors
nobs3 = mod.nobs ## Number of observations

## Save the fitted values from first stage as mpg_hat
#IvData3['mpghat'] = beta_FS3[0] + (beta_FS3[1]* IvData3['treatment'])+ (beta_FS3[2]*IvData3['length'])

IvData31 = IvData3.loc[(IvData3['treatment'] == 0)]
IvData31['mpghat'] = beta_FS3[0] +  (beta_FS3[2]*IvData31['length'])

IvData32 = IvData3.loc[(IvData3['treatment'] == 1)]
IvData32['mpghat'] = beta_FS3[0] + beta_FS3[1] + (beta_FS3[2]*IvData32['length'])


## Plot the resulting polynomial over a scatterplot
plt.figure(figsize=(12, 8))
plt.scatter(IvData3['length'],IvData3['mpg'], facecolors='none', edgecolors='r') ## Scatter plot
plt.axvline(x=threshold, color='b') #a line at the RD cutoff
plt.plot(IvData31['length'], IvData31['mpghat'], color='green') #Fitted line
plt.plot(IvData32['length'], IvData32['mpghat'], color='green') #Fitted line
plt.xlabel("Length")
plt.ylabel("Fuel efficiency (mpg")

plt.savefig('discontinuity_3.pdf',format='pdf')

## Build output table
### Reorder output (I probably should figure out a way to do this all at once)
order3 = np.array([1,2,0])
beta_FS3 = beta_FS3[order3]
stderr3 = stderr3[order3]


### Row and column names
rownames3 = pd.concat([pd.Series(['Treated', 'length', 'Constant', 'Observations']),pd.Series([' ',' ',' '])],axis = 1).stack()
colnames3 = pd.Series(['Coefficients'])


### Stack estimates over Standard Errors
cola= pd.concat([beta_FS3, stderr3],axis = 1).stack()
cola = pd.Series(np.append(cola, nobs3))

### Format Standard Errors
stderr3 = pd.Series(np.round(stderr3,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
beta_FS3 = pd.Series(np.append(np.round(beta_FS3,2), nobs3))
stderr3  = stderr3 .map('({:.2f})'.format)

### Stack estimates over Standard Errors
col3a = pd.concat([beta_FS3,stderr3],axis = 1).stack()
o3 = np.array([])

### Output
col3a.index = rownames3
col3a.columns = colnames3

print(col3a)

col3a.to_latex('RD3_python.tex')

#*************************************************************************************************
#plt.figure(figsize=(12, 8))
#plt.scatter(IvData3['length'],IvData3['mpghat'], facecolors='none', edgecolors='r')

#plt.axvline(x=threshold, color='b') #a line at the RD cutoff
#plt.plot(IvData31['length'], IvData31['mpghat'], color='blue')
#plt.plot(IvData32['length'], IvData32['mpghat'], color='blue')

##############################################################################################
#****************************** Question 4  ***************************#

IvData4 = IvData

IvData4['length_sq'] = IvData4['length'] * IvData4['length']

## Fit into RDD model
model = rdd.rdd(IvData4, 'length_sq', 'mpg', cut=threshold*threshold)
mod=model.fit()
print(mod.summary())

beta_FS4 = mod.params # Save the coeffcients from the first stage

IvData41 = IvData4.loc[(IvData4['treatment'] == 0)]
IvData41['mpghat'] = beta_FS4[0] +  (beta_FS4[2]*IvData41['length_sq'])

IvData42 = IvData4.loc[(IvData4['treatment'] == 1)]
IvData42['mpghat'] = beta_FS4[0] + beta_FS4[1] + (beta_FS4[2]*IvData42['length_sq'])


IvData4['mpghat'] = beta_FS4[0] + (beta_FS4[1]* IvData4['treatment'])+ (beta_FS4[2]*IvData4['length'])

## Plot the resulting polynomial over a scatterplot
plt.figure(figsize=(12, 8))
plt.scatter(IvData4['length_sq'],IvData4['mpg'], facecolors='none', edgecolors='r')
plt.axvline(x=threshold*threshold, color='b') #a line at the RD cutoff
plt.plot(IvData41['length_sq'], IvData41['mpghat'], color='green') #Fitted line
plt.plot(IvData42['length_sq'], IvData42['mpghat'], color='green') #Fitted line
plt.xlabel("Length_sq")
plt.ylabel("Fuel efficiency (mpg")


plt.savefig('discontinuity_4.pdf',format='pdf')



##############################################################################################
#****************************** Question 5  ***************************#

IvData5 = IvData

IvData5['length_fv'] = IvData5['length'] * IvData5['length'] * IvData5['length'] * IvData5['length'] * IvData5['length'] 

## Fit into RDD model
threshold5 = threshold * threshold * threshold * threshold * threshold 

model = rdd.rdd(IvData5, 'length_fv', 'mpg', cut=threshold5)
mod=model.fit()
print(mod.summary())

beta_FS5 = mod.params # Save the coeffcients from the first stage

## Save the fitted values from first stage as mpg_hat
IvData5['mpghat'] = beta_FS5[0] + (beta_FS5[1]* IvData5['treatment'])+ (beta_FS5[2]*IvData5['length_fv'])

IvData51 = IvData5.loc[(IvData5['treatment'] == 0)]
IvData51['mpghat'] = beta_FS5[0] +  (beta_FS5[2]*IvData51['length_fv'])

IvData52 = IvData5.loc[(IvData5['treatment'] == 1)]
IvData52['mpghat'] = beta_FS5[0] + beta_FS5[1] + (beta_FS5[2]*IvData52['length_fv'])


## Plot the resulting polynomial over a scatterplot
plt.figure(figsize=(12, 8))
plt.scatter(IvData5['length_fv'],IvData5['mpg'], facecolors='none', edgecolors='r')
plt.axvline(x=threshold5, color='b') #a line at the RD cutoff
plt.plot(IvData51['length_fv'], IvData51['mpghat'], color='green') #Fitted line
plt.plot(IvData52['length_fv'], IvData52['mpghat'], color='green') #Fitted line
plt.xlabel("Length^5")
plt.ylabel("Fuel efficiency (mpg")


plt.savefig('discontinuity_5.pdf',format='pdf')


##############################################################################################
#****************************** Question 6  ***************************#


IvData6 = IvData

## Fit into RDD model
model = rdd.rdd(IvData6, 'length', 'mpg', cut=threshold)
mod=model.fit()
print(mod.summary())

beta_FS6 = mod.params # Save the coeffcients from the first stage
stderr6 = mod.bse ## Extract the standard errors
nobs6 = mod.nobs ## Number of observations

## Save the fitted values from first stage as mpg_hat
IvData6['mpghat'] = beta_FS6[0] + (beta_FS6[1]* IvData6['treatment'])+ (beta_FS6[2]*IvData6['length'])

## Second stage
IvData6 = IvData6[["price", "mpg", "height", "length", "weight", "mpghat", "car"]]

## Second stage: price regression using fitted values from the first stage
SecondS_6 = sm.OLS(IvData6['price'],sm.add_constant(IvData6.drop(['price', 'mpg', 'height', 'length', 'weight'],axis = 1))).fit()
print(SecondS_6.summary())

beta_SS6 = SecondS_6.params # Save the coeffcients from the second stage
std_SS6 = SecondS_6.bse ## Extract the standard errors
nobs6 = SecondS_6.nobs ## Number of observations















