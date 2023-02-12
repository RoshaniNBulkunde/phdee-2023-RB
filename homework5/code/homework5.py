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

# Set working directories and seed

datapath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework5'
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework5\output'

os.chdir(datapath) # To change the current working directory to specified path

## Import kwh.csv data
IvData = pd.read_csv('C:\\Users\\rosha\\Dropbox (GaTech)\\PhD-2023-Env2\\phdee-2023-RB\\homework5\\instrumentalvehicles.csv')