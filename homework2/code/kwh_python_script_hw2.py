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

# Set working directories and seed

## The "outputpath" is where I will export my outputs
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework2\output'

#Create a table that displays each variable’s sample mean, sample standard deviation, and p-values for the two-way t-test between
#treatment and control group means

## Import kwh.csv data
kwhData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework2\\kwh.csv')

## Just to view summary statistics
print(kwhData.describe())
#print(kwhData.groupby('retrofit').mean()
## Generate means
means = kwhData.mean()

## Generate standard deviations
stdev = kwhData.std()

## Get number of observations
nobs2 = kwhData.count().min()

## Set the row and column names
rownames = pd.concat([pd.Series(['Electricity','Home', 'Temperature', 'Observations']),pd.Series([' ', ' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
colnames = [('Mean','(s.d.)')] # Two rows of column names

## Format means and std devs to display to two decimal places
#means = means.map('{:.2f}'.format)
#stdev = stdev.map('({:.2f})'.format)

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 10:26:00 2023

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

# I need to created the separate columns with variable names with sample mean and standard deviation for control group 
## Generate means for control group
meansControl = kwhData[kwhData["retrofit"]==0].mean()

## Generate standard deviations for control group
stdevControl = kwhData[kwhData["retrofit"]==0].std()

## Get number of observations for control group
nobs2Control = kwhData[kwhData["retrofit"]==0].count().min()

# I need to created the separate columns with variable names with sample mean and standard deviation for treatment group 
## Generate means for treatment group
meansTreatment = kwhData[kwhData["retrofit"]==1].mean()

## Generate standard deviations for treatment group
stdevTreatment = kwhData[kwhData["retrofit"]==1].std()

## Get number of observations for treatment group
nobs2Treatment = kwhData[kwhData["retrofit"]==1].count().min()


control = kwhData[kwhData['retrofit']==0]
treat = kwhData[kwhData['retrofit']==1]
electricity_test = ttest_ind(treat['electricity'], control['electricity'])
electricity_test = e_t_test = pd.DataFrame(electricity_test)

sq_control = kwhData[kwhData['retrofit']==0]
sq_treat = kwhData[kwhData['retrofit']==1]
sq_ttest = ttest_ind(sq_treat['sqft'], sq_control['sqft'])
sq_ttest = pd.DataFrame(sq_ttest)

retrofit_ttest = ttest_ind(sq_treat['retrofit'], sq_control['retrofit'])
retrofit_ttest = pd.DataFrame(retrofit_ttest)

temp_ttest = ttest_ind(sq_treat['temp'], sq_control['temp'])
temp_ttest = pd.DataFrame(temp_ttest)


## Set the row and column names
rownames = pd.concat([pd.Series(['Electricity','Home', 'Retrofit', 'Temperature', 'Observations']),pd.Series([' ',' ', ' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
colnames = [('Mean','(s.d.)')] # Two rows of column names

## Align std deviations under means and add observations
col0 = pd.concat([meansControl,stdevControl,pd.Series(nobs2Control)],axis = 1).stack()
col1 = pd.concat([meansTreatment,stdevTreatment,pd.Series(nobs2Treatment)],axis = 1).stack()
col2 = pd.concat([electricity_test, sq_ttest, retrofit_ttest, temp_ttest, pd.Series(nobs2Control)], axis = 0)

## Add column and row labels.  Convert to dataframe (helps when you export it)
col0 = pd.DataFrame(col0)
col0.index = rownames
col0.columns = pd.MultiIndex.from_tuples(colnames)


col1 = pd.DataFrame(col1)
col1.index = rownames
col1.columns = pd.MultiIndex.from_tuples(colnames)


col2 = pd.DataFrame(col2)
col2.index = rownames
col2.columns = pd.MultiIndex.from_tuples(colnames)


merged_col = pd.concat([col0, col1, col2], axis = 1)

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

merged_col.to_latex('samplemeantable.tex') # Note you would have to stitch together multiple series into a dataframe to have multiple columns

