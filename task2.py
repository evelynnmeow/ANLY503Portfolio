#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:51:25 2020

@author: jingjiema
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read in the data
accounts = pd.read_csv("data/accounts_analytical.csv")
# drop missing values
df = accounts[pd.notnull(accounts['loan_amount'])]
# convert the string of date to datetime format
df['loan_date_new'] = pd.to_datetime(df['loan_date'])

# plot the distribution of loan amount
df.plot(y = 'loan_amount', kind = 'hist')
plt.title('Distribution of Loan Amount')
plt.xlabel('Loan Amount')
plt.ylabel('Frequeny')
#plt.show()

# Distribution of loan term
df.plot.hist(y='loan_term')
plt.title('Distribution of Loan term')
plt.xlabel('Loan term')
plt.ylabel('Frequeny')
plt.show()


# Distribution of loan payment
df.plot.hist(y='loan_payment')
plt.title('Distribution of Loan payment')
plt.xlabel('Loan payment')
plt.ylabel('Frequeny')
plt.show()

# Distribution of loan default
df['loan_default'].value_counts().plot(kind='bar', alpha=0.75, rot=0)
plt.title('Distribution of Loan default')
plt.xlabel('Loan default')
plt.ylabel('Frequeny')
plt.show()

# Distribution of loan status
df['loan_status'].value_counts().plot(kind='bar', alpha=0.75, rot=0)
plt.title('Distribution of Loan status')
plt.xlabel('Loan status')
plt.ylabel('Frequeny')
plt.show()

# Distribution of loan date
#df.plot.hist(y='loan_date_new')
fig, ax = plt.subplots()
df["loan_date_new"].astype(np.int64).plot.hist(ax=ax)
labels = ax.get_xticks().tolist()
labels = pd.to_datetime(labels)
ax.set_xticklabels(labels, rotation=90)
plt.title('Distribution of Loan date')
plt.xlabel('Loan date')
plt.ylabel('Frequeny')
plt.show()






