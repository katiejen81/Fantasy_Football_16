
# Program Information -----------------------------------------------------

#Prepare Data For Analysis
#KTanner 8/13


# Install needed packages -------------------------------------------------

#install.packages("sqldf")
#install.packages("RSQLite")
library("sqldf")
library("RSQLite")


# Bring in csv file -------------------------------------------------------

#nfldata <- read.csv('C:/Users/Katie/Documents/Fantasy_Football_16/full_stats.csv')

nfldata <- read.csv('/home/katie/Fantasy Football Programs and Files/full_stats.csv')

#Dedupe the list - there are upwards of 4 duplicates :(

nfldata2 <- sqldf("SELECT DISTINCT * FROM nfldata WHERE gsisPlayerID <> 'False'")


# Calculate FF Points for the Game ----------------------------------------

#Let's first start by finding the column names for everyone so that I can convert them to points

stats <- as.data.frame(names(nfldata2))

#And now let's get the point values from the Fantasy League

Points <- read.csv('/home/katie/Fantasy Football Programs and Files/Fantasy_Point_Values.csv')

#Offensive Points - R Studio appears to only show 100 variables whewn looking at data. Print the column to see the value


#passing yards
nfldata2$Points_Passing_Yards <- round(nfldata2$Pass_Yds/25)
nfldata2$Points_Passing_Yards

#passing TD
nfldata2$Points_Passing_TD <- round(nfldata2$Pass_TD * 4)
nfldata2$Points_Passing_TD

#Passing Interceptions
nfldata2$Points_Passing_Int <- round(nfldata2$Pass_Int * -1)
nfldata2$Points_Passing_Int

#Rushing Yards
nfldata2$Points_Rushing_Yards <- round(nfldata2$Rush_Yds/10)
nfldata2$Points_Rushing_Yards

#Rushing Touchdowns
nfldata2$Points_Rushing_TD <- round(nfldata2$Rush_TD * 6)
nfldata2$Points_Rushing_TD

#Receptions
nfldata2$Points_Reception <- round(nfldata2$Receptions * 1)
nfldata2$Points_Reception

#Receiving Touchdowns
nfldata2$Points_Receiving_TD <- round(nfldata2$Rec_TD * 6)
nfldata2$Points_Receiving_TD

#Return Touchdowns
nfldata2$Points_Return_TD <- round(nfldata2$Return_TD * 6)
nfldata2$Points_Return_TD

#Two Point Conversions
nfldata2$Points_Two_Pt_Conv <- round(nfldata2$X2PT * 2)
nfldata2$Points_Two_Pt_Conv

#Fumbles Lost
nfldata2$Points_Fumble_Lost <- round(nfldata2$Fum_Lost * -2)
nfldata2$Points_Fumble_Lost

#Offensive Fumble Return TD
nfldata2$Points_Fumble_Return_TD <- round(nfldata2$Fum_TD * 6)
nfldata2$Points_Fumble_Return_TD