#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:18:00 2020

@author: jingjiema
"""

import pandas as pd
import numpy as np

# read in the file
loans = pd.read_csv("data/loans.csv")
# pivot the dataframe to get loans info
df = loans.melt(id_vars = ['id', 'account_id', 'date', 'amount', 'payments'], var_name = 'demo', 
                value_name='status')
df.head(3)
# use regex to extract the duration and type
tmp=df.demo.str.split('([0-9][0-9])[_]([A-Z])', expand=True)

tmp.columns = ['None','duration', 'type', 'None']
df1 = pd.concat([df.drop('demo', axis=1),tmp.iloc[:,1:4]], axis=1)
df2 = df1.drop(columns=['None'])
# drop rows with inactive loans
final = df2.loc[df2['status'] == 'X']

# write to csv
final.to_csv('loans_py.csv', index=None)