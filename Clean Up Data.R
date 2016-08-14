
# Program Information -----------------------------------------------------

#Prepare Data For Analysis
#KTanner 8/13


# Install needed packages -------------------------------------------------

install.packages("sqldf")
install.packages("RSQLite")
library("sqldf")
library("RSQLite")


# Bring in csv file -------------------------------------------------------

nfldata <- read.csv('C:/Users/Katie/Documents/Fantasy_Football_16/full_stats.csv')

#Dedupe the list - there are upwards of 4 duplicates :(

nfldata2 <- dbgetquery(nfldata, "SELECT DISTINCT *")
