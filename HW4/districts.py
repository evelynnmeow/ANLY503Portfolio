#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:48:52 2020

@author: jingjiema
"""

import pandas as pd
import numpy as np

# read in the file
districts = pd.read_csv("data/districts.csv")

# melt the data tp get population info
df = districts.melt(id_vars = ['id', 'name', 'region', 'population',
                               'num_cities', 'urban_ratio', 'entrepreneur_1000',
                               'unemployment_rate', 'commited_crimes'], value_vars = ['municipality_info'],
                    var_name = 'demo', value_name='status')

tmp=df.status.str.split('\\[([0-9]+)[,]+([0-9]+)[,]+([0-9]+)[,]+([0-9]+)\\]', expand = True)
tmp.columns = ['None','pop_lessn_500', 'pop_500_1999', 'pop_2000_9999', 
               'pop_greater_10000', 'None']

df1 = pd.concat([df.drop('status', axis=1),tmp.iloc[:,1:6]], axis=1)
# df2 is the final dataframe for now
df2 = df1.drop(columns=['None','demo'])

# melt the data again to get unemployment info
df3 = df2.melt(id_vars = ['id', 'name', 'region', 'population',
                               'num_cities', 'urban_ratio', 'entrepreneur_1000',
                               'commited_crimes', 'pop_lessn_500', 'pop_500_1999', 'pop_2000_9999', 
                               'pop_greater_10000'], value_vars = ['unemployment_rate'],
                    var_name = 'demo', value_name='status')

tmp1 = df3.status.str.split('\\[([0-9]+.[0-9]+)[,]+([0-9].[0-9]+)\\]', expand = True)
tmp1.columns = ['None','unemployment_rate_95', 'unemployment_rate_96', 'None']
df4 = pd.concat([df3.drop('status', axis=1),tmp1.iloc[:,1:4]], axis=1)
# df5 is the final dataframe till now
df5 = df4.drop(columns=['demo', 'None'])


# melt data to get the crime info
df6 = df5.melt(id_vars = ['id', 'name', 'region', 'population',
                               'num_cities', 'urban_ratio', 'entrepreneur_1000',
                               'pop_lessn_500', 'pop_500_1999', 'pop_2000_9999', 
                               'pop_greater_10000', 'unemployment_rate_95', 
                               'unemployment_rate_96'], value_vars = ['commited_crimes'],
                    var_name = 'demo', value_name='status')

tmp2 = df6.status.str.split('\\[([0-9]+)[,]+([0-9]+)\\]', expand = True)
tmp2.columns = ['None','commited_crimes_95', 'commited_crimes_96', 'None']
df7 = pd.concat([df6.drop('status', axis=1),tmp2.iloc[:,1:4]], axis=1)
# df8 is the final dataframe till now
df8 = df7.drop(columns=['demo', 'None'])


# write to csv without adding extra indices
df8.to_csv('district_py.csv', index=None)

