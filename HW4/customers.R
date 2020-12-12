library(tidyverse)

# read in the accounts data
accounts = read.csv('data/accounts.csv')
head(accounts)

# read in the cliencts data
clients = read.csv('data/clients.csv')
head(clients)

# read in the links data
links = read.csv('data/links.csv')
head(links)

# read in the transaction data
transactions = read.csv('data/transactions.csv')
head(transactions)
str(transactions)
unique(transactions$method)
unique(transactions$category)

# read in the districts data
districts = read.csv('district_r.csv')
head(districts)

# read in the cards data
cards = read.csv('data/cards.csv')
head(cards)

# read in the loans sdata
loans = read.csv('loans_r.csv')
head(loans)

# left join the accounts data to the district data to get the district name
# and drop all cols that are irrelevant
df = accounts %>% left_join(districts, by = c("district_id" = "id")) %>%
  select(id, name, date, statement_frequency) 
head(df)

names(df)[names(df) == "id"] <- "account_id"
names(df)[names(df) == "name"] <- "district_name"
names(df)[names(df) == "date"] <- "open_date"
head(df)

# manipulate the links table to get the number of customers
# df1 will only contain account id and num customers
df1 = links %>% 
  mutate(uniq_client = ifelse(is.na(client_id), 0, 1)) %>%
  group_by(account_id) %>%
  summarise(num_customers = sum(uniq_client))
  
head(df1)


# left join df and df1 to find ways connecting clients and accounts
# df2 is the end result till now
df2 = df %>% left_join(df1, by = "account_id")
head(df2)

head(cards)
#temp = df3 = df2 %>% left_join(cards, by = c("account_id" = "link_id"))
# join cards with links to get number of cards for each account
df3 = df2 %>% left_join(cards, by = c("account_id" = "link_id")) %>%
  mutate(uniq_id = ifelse(is.na(id.y), 0, 1)) %>%
  group_by(account_id) %>%
  summarise(credit_cards = sum(uniq_id))
  
head(df3)

# joint df3 with df2 to get number of credit cards
# df4 is the end result till now
df4 = df2 %>% left_join(df3, by = "account_id")
head(df4)

#temp1 = df5 = df4 %>% full_join(loans, by = "account_id")  %>%
  #mutate(loan = ifelse(is.na(id.y), FALSE, TRUE))
# outer join df4 and loans to get the info of loans
# df 5 is the end result till now
df5 = df4 %>% full_join(loans, by = "account_id") %>%
  mutate(loan = ifelse(is.na(id.y), FALSE, TRUE)) %>% 
  mutate(loan_status = case_when(type == "A"|type == "B" ~ "expired",
                                 type == "C" | type == "D" ~ "current")) %>%
  mutate(loan_default = case_when(type == "B"|type == "D" ~ TRUE,
                                  type == "A" | type == "C" ~ FALSE)) 
  

# change col names of df5
names(df5)[names(df5) == "amount"] <- "loan_amount"
names(df5)[names(df5) == "payments"] <- "loan_payments"
names(df5)[names(df5) == "duration"] <- "loan_term"
df5 = df5 %>% select(account_id, district_name, open_date, statement_frequency, 
                     num_customers, credit_cards, loan, loan_amount, loan_payments, loan_term,
                     loan_status, loan_default)
head(df5)

# add transaction info
print(transactions)
df_trans = transactions %>% group_by(account_id) %>% 
  summarise(max_withdrawal = max(amount), min_withdrawal = min(amount),
            max_balance = max(balance), min_balance = min(balance),
            cc_payment = sum(type=="credit"))
head(df_trans)
# merge df_trans and df5
# df6 is the final result till now
df6 = df5 %>% left_join(df_trans, by = "account_id")
head(df6)

# write to csv without adding extra indices
write.csv(df6, 'customers_r.csv', row.names=FALSE)
