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

# The "outputpath" is where I will export my outputs
outputpath = r'C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework2\output'

#Import kwh.csv data
