library(tidyverse)

# read in the data
loan = read.csv("data/loans.csv")
head(loan)
#
# collect information of loands
df1 = loan %>% pivot_longer(cols = X24_A:X60_A, names_to = 'demo', values_to = 'status')
head(df1)
# extract the loan type and duration
f2 = df1 %>% 
  extract(demo, c('duration', 'type'), regex = 'X([0-9][0-9])[_]([A-Z])')
head(f2)
# Since one account can only have one load, drop any loan that status is not X
# also drop the status col since it is irrelevant
loan_final = f2 %>% filter(status== 'X') %>% select(-status)
head(loan_final)

# read to csv without adding extra indices
write.csv(loan_final, 'loans_r.csv', row.names=FALSE)

