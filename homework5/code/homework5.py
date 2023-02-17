# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:02:55 2023

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

# Set working directories and seed

datapath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework5'
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework5\output'

os.chdir(datapath) # To change the current working directory to specified path

## Import kwh.csv data
IvData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework5\\instrumentalvehicles.csv')

##########################################################################################################################

#****************************** Question 1 ***************************#

## Direct method
ols_q1 = sm.OLS(IvData['price'],sm.add_constant(IvData.drop(['price', 'weight', 'height', 'length'],axis = 1))).fit()
print(ols_q1.summary())
olsbeta_q1 = ols_q1.params


#****************************** Question 2--part (a) ***************************#

IvData2a = IvData[["price", "mpg", "height", "length", "weight", "car"]]
 
## First Stage: regress mpg using weight as the excluded instrument
FirstS_2a = sm.OLS(IvData2a['mpg'],sm.add_constant(IvData2a.drop(['price', 'mpg', 'height', 'length'],axis = 1))).fit()
print(FirstS_2a.summary())

## Extracting the data needto build the table
beta_FS_2a = FirstS_2a.params # Save the coeffcients from the first stage
##FirstS_2a.fvalue #For f-statistics
fres = FirstS_2a.f_test("weight=0") # F-statistic for the excluded instrument
fstat_2a = fres.fvalue

## Save the fitted values from first stage as mpg_hat
IvData2a['mpghat'] = beta_FS_2a[0] + (beta_FS_2a[1]* IvData2a['weight'])+ (beta_FS_2a[2]*IvData2a['car'])

IvData2a = IvData2a[["price", "mpg", "height", "length", "weight", "mpghat", "car"]]

## Second stage: price regression using fitted values from the first stage
SecondS_2a = sm.OLS(IvData2a['price'],sm.add_constant(IvData2a.drop(['price', 'mpg', 'height', 'length', 'weight'],axis = 1))).fit()
print(SecondS_2a.summary())

beta_SS_2a = SecondS_2a.params # Save the coeffcients from the second stage
std_SS2a = SecondS_2a.bse ## Extract the standard errors
nobs2a = SecondS_2a.nobs ## Number of observations

### Format Standard Errors
std_SS2a = pd.Series(np.round(std_SS2a,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
beta_SS_2a = pd.Series(np.round(beta_SS_2a,2))
# beta_SS_2a = pd.Series(np.append(np.round(beta_SS_2a,2), nobs2a))
std_SS2a  = std_SS2a.map('({:.2f})'.format)


### Stack estimates over Standard Errors
cola= pd.concat([beta_SS_2a, std_SS2a],axis = 1).stack()
cola = pd.Series(np.append(cola, nobs2a))
cola = pd.Series(np.append(cola, fstat_2a))

#****************************** Question 2--part (b) ***************************#

IvData2b = IvData

## Create a variabel weight square
IvData2b['weight_sq'] = IvData2b['weight'] * IvData2b['weight']

IvData2b = IvData[["price", "mpg", "height", "length", "weight", "weight_sq", "car"]] #Rearrage the order

## First Stage: regress mpg using weight square as the excluded instrument
FirstS_2b = sm.OLS(IvData2b['mpg'],sm.add_constant(IvData2b.drop(['price', 'mpg', 'height', 'length', 'weight'],axis = 1))).fit()
print(FirstS_2b.summary())
beta_FS_2b = FirstS_2b.params # Save the coeffcients from the first stage

fres = FirstS_2b.f_test("weight_sq=0") # F-statistic for the excluded instrument
fstat_2b = fres.fvalue

## Save the fitted values from first stage as mpg_hat
IvData2b['mpghat'] = beta_FS_2b[0] + (beta_FS_2b[1]* IvData2b['weight_sq'])+ (beta_FS_2b[2]*IvData2b['car'])

IvData2b = IvData2b[["price", "mpg", "height", "length", "weight", "mpghat", "weight_sq", "car"]]

## Second stage: price regression using fitted values from the first stage
SecondS_2b = sm.OLS(IvData2b['price'],sm.add_constant(IvData2b.drop(['price', 'mpg', 'height', 'length', 'weight', 'weight_sq'],axis = 1))).fit()
print(SecondS_2b.summary())

beta_SS_2b = SecondS_2b.params # Save the coeffcients from the second stage
std_SS2b = SecondS_2b.bse ## Extract the standard errors
nobs2b = SecondS_2b.nobs ## Number of observations

### Format Standard Errors
std_SS2b = pd.Series(np.round(std_SS2b,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
beta_SS_2b = pd.Series(np.round(beta_SS_2b,2))
# beta_SS_2a = pd.Series(np.append(np.round(beta_SS_2a,2), nobs2a))
std_SS2b  = std_SS2b.map('({:.2f})'.format)


### Stack estimates over Standard Errors
colb= pd.concat([beta_SS_2b, std_SS2b],axis = 1).stack()
colb = pd.Series(np.append(colb, nobs2b))
colb = pd.Series(np.append(colb, fstat_2b))

#****************************** Question 2--part (c) ***************************#

IvData2c = IvData[["price", "mpg", "length", "height", "weight", "car"]] #Rearrange the order

## First Stage: regress mpg using height as the excluded instrument
FirstS_2c = sm.OLS(IvData2c['mpg'],sm.add_constant(IvData2c.drop(['price', 'mpg', 'length', 'weight'],axis = 1))).fit()
print(FirstS_2c.summary())
beta_FS_2c = FirstS_2c.params # Save the coeffcients from the first stage

fres = FirstS_2c.f_test("height=0") # F-statistic for the excluded instrument
fstat_2c = fres.fvalue


## Save the fitted values from first stage as mpg_hat
IvData2c['mpghat'] = beta_FS_2c[0] + (beta_FS_2c[1]* IvData2c['height'])+ (beta_FS_2c[2]*IvData2c['car'])

IvData2c = IvData2c[["price", "mpg", "height", "length", "weight", "mpghat", "car"]]

## Second stage: price regression using fitted values from the first stage
SecondS_2c = sm.OLS(IvData2c['price'],sm.add_constant(IvData2c.drop(['price', 'mpg', 'height', 'length', 'weight'],axis = 1))).fit()
print(SecondS_2c.summary())

beta_SS_2c = SecondS_2c.params # Save the coeffcients from the second stage
std_SS2c = SecondS_2c.bse ## Extract the standard errors
nobs2c = SecondS_2c.nobs ## Number of observations

### Format Standard Errors
std_SS2c = pd.Series(np.round(std_SS2c,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
beta_SS_2c = pd.Series(np.round(beta_SS_2c,2))
# beta_SS_2a = pd.Series(np.append(np.round(beta_SS_2a,2), nobs2a))
std_SS2c  = std_SS2c.map('({:.2f})'.format)


### Stack estimates over Standard Errors
colc= pd.concat([beta_SS_2c, std_SS2c],axis = 1).stack()
colc = pd.Series(np.append(colc, nobs2c))
colc = pd.Series(np.append(colc, fstat_2c))

### Bulding table
cola=pd.DataFrame(cola)
colb=pd.DataFrame(colb)
colc=pd.DataFrame(colc)

Col4 = pd.concat([cola,colb,colc], axis = 1)

rownames = pd.concat([pd.Series(['Constant', 'Fuel Efficiency (mpg)', 'Car', 'Observations', 'F-statistics']),pd.Series([' ',' ',' '])],axis = 1).stack()
rownames = rownames.reset_index()
rownames =rownames[0]

colnames = pd.Series(['(3a)','(3b)','(3c)'])
Col4.columns = colnames

Col4.index = rownames

os.chdir(outputpath)
Col4.to_latex('output3_python.tex')

######################################################################################################

#****************************** Question 4 ***************************#
IvData["const"] = 1 ## Add constant
Xvar = IvData[["const", "car"]] #Exogenous variable


ivmod = IVGMM(IvData.price, Xvar, IvData.mpg, IvData[["weight"]]) ##Fit in the GMM model
res_gmm = ivmod.fit()

print(res_gmm)

## Extract the data
beta_gmm = res_gmm.params # Save the coeffcients from the second stage
std_gmm = res_gmm.std_errors ## Extract the standard errors
nobsgmm = res_gmm.nobs ## Number of observations

### Format Standard Errors
std_gmm = pd.Series(np.round(std_gmm,2)) # Rounds to two decimal places and puts into a Series

### Format estimates and append observations
beta_gmm = pd.Series(np.round(beta_gmm,2))
std_gmm  = std_gmm.map('({:.2f})'.format)

### Stack estimates over Standard Errors
cold= pd.concat([beta_gmm, std_gmm],axis = 1).stack()
cold = pd.Series(np.append(cold, nobsgmm))

rownames1 = pd.concat([pd.Series(['Constant', 'Fuel Efficiency (mpg)', 'Car', 'Observations']),pd.Series([' ',' ',' '])],axis = 1).stack()

colnames1 = pd.Series(['(4a)'])
cold.columns = colnames1

cold.index = rownames1

os.chdir(outputpath)
cold.to_latex('IVGMM_python.tex')