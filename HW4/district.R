library(tidyverse)

# read in the data
df = read.csv('data/districts.csv')
str(df)

# extract info of municipality info column
df1 = df %>% 
  extract(municipality_info, 
          c('pop_lessn_500', 'pop_500_1999', 'pop_2000_9999', 'pop_greater_10000'), 
          regex = '\\[([0-9]+)[,]+([0-9]+)[,]+([0-9]+)[,]+([0-9]+)\\]')
head(df1)

# extract the unemployment rate from 95 and 96
df2 = df1 %>% 
  extract(unemployment_rate, c('unemployment_rate_95', 'unemployment_rate_96'),
          regex = '\\[([0-9]+.[0-9]+)[,]+([0-9].[0-9]+)\\]')
head(df2)

# extract commited crimes from 95 and 96
df3 = df2 %>% 
  extract(commited_crimes, c('commited_crimes_95', 'commited_crimes_96'), 
          regex = '\\[([0-9]+)[,]+([0-9]+)\\]')

head(df3)

# write to csv without adding extra indices
write.csv(df3, 'district_r.csv', row.names=FALSE)




