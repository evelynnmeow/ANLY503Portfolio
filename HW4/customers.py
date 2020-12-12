#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:53:03 2020

@author: jingjiema
"""

import pandas as pd
import numpy as np

# read in the data
accounts = pd.read_csv('data/accounts.csv')
clients = pd.read_csv('data/clients.csv')
links = pd.read_csv('data/links.csv')
transactions = pd.read_csv('data/transactions.csv')
districts = pd.read_csv('district_py.csv')
cards = pd.read_csv('data/cards.csv')
loans = pd.read_csv('loans_py.csv')

# left join the accounts data to the district data to get the district name
# and drop all cols that are irrelevant
df = accounts.join(districts.set_index('id'), on='district_id', how = 'left')
# df1 is the final product till now
df1 = df[['id', 'name', 'date', 'statement_frequency']]
df1 = df1.rename(columns={"id": "account_id", "name": "district_name", "date": "open_date"})


# manipulate the links table to get the number of customers
condition1 = (links["client_id"].isnull())
condition2 = (links["client_id"].notnull())
choices = [0, 1]

conditions = [condition1, condition2]
links['uniq_customer'] = np.select(conditions, choices, default="")
links['num_customers'] = links.groupby("account_id")["uniq_customer"].transform("count")
#df2 is the final product till now
df2 = pd.merge(df1, links, on='account_id', how = "left")
df2 = df2[['account_id', 'district_name', 'open_date', 'statement_frequency','num_customers']]
df2 = df2.drop_duplicates(subset='account_id', keep="last")


# join cards with links to get number of cards for each client
# df3 only contains account id and num customer
df3 = pd.merge(df2, cards,left_on='account_id',right_on='link_id', how = "left")
condition1 = (df3["id"].isnull())
condition2 = (df3["id"].notnull())
choices = [0, 1]

conditions = [condition1, condition2]
df3['uniq_id'] = np.select(conditions, choices, default="")
df3['credit_cards'] = df3.groupby('account_id')['uniq_id'].transform('sum') 
df3 = df3[['account_id','credit_cards']]
df3 = df3.drop_duplicates(subset='account_id', keep="last")
# join df2 and df3
df4 = pd.merge(df2, df3,on='account_id', how = "left")
# df4 is the final product till now
df4 = df4[['account_id', 'district_name', 'open_date', 'statement_frequency','num_customers','credit_cards']]


# full join df4 and loans to get the info of loans
# df 5 is the end result till now
df5 = pd.merge(df4, loans,on='account_id', how = "outer")
condition1 = (df5["id"].isnull())
condition2 = (df5["id"].notnull())
choices = [False, True]
conditions = [condition1, condition2]
df5['loans'] = np.select(conditions, choices, default="")
condition_one = (df5["type"] == 'A') | (df5["type"] == 'B')
condition_two = (df5["type"] == 'C') | (df5["type"] == 'D')
condition_three = (df5["type"].isnull())
choices = ["expired", "current", np.nan]
conditions = [condition_one, condition_two, condition_three]
df5['loan_status'] = np.select(conditions, choices, default="")
condition4 = (df5["type"] == 'B') | (df5["type"] == 'D')
condition5 = (df5["type"] == 'A') | (df5["type"] == 'C')
condition6 = (df5["type"].isnull())
choices1 = [True, False, np.nan]
conditions1 = [condition4, condition5, condition6]
df5['loan_default'] = np.select(conditions1, choices1, default="")

# rename the cols
df5 = df5.rename(columns={"amount": "loan_amount", "payments": "loan_payments",  "duration": "loan_term"})
df5 = df5[['account_id', 'district_name', 'open_date', 'statement_frequency','num_customers','credit_cards', 'loans', "loan_amount","loan_payments", "loan_term", "loan_status", "loan_default"]]

# add transaction info
# df6 is final product till now
# first manipulate transactions for cc, min, max info
print(transactions.head())
transactions['cc_payments'] = transactions[transactions['type']=="credit"].any(axis=1)
print(transactions.head())
# get cc_payments
trans_df = transactions.groupby('account_id')['cc_payments'].agg('sum').reset_index()
# get max_balance
trans_df1 = transactions.groupby('account_id')['balance'].agg('max').reset_index()
trans_df1 = trans_df1.rename(columns={"balance": "max_balance"})
# get min_balance
trans_df2 = transactions.groupby('account_id')['balance'].agg('min').reset_index()
trans_df2 = trans_df2.rename(columns={"balance": "min_balance"})
# get df6
df6 = pd.merge(df5, trans_df,on='account_id', how = "left")
df6 = pd.merge(df6, trans_df1,on='account_id', how = "left")
df6 = pd.merge(df6, trans_df2,on='account_id', how = "left")

# write to csv without adding extra index
df6.to_csv('customers_py.csv', index=None)


