
# Program Information -----------------------------------------------------

#Prepare Data For Analysis
#KTanner 8/13


# Install needed packages -------------------------------------------------

#install.packages("sqldf")
#install.packages("RSQLite")
#install.packages('plyr')
library("sqldf")
library("RSQLite")
library('plyr')


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

#Kickers Field Goals 0-19 yds
nfldata2$Points_FG_0_19 <- round(nfldata2$FG_0.19 * 3)
nfldata2$Points_FG_0_19

#Kickers Field Goals 20-29 yds
nfldata2$Points_FG_20_29 <- round(nfldata2$FG_20.29 * 3)
nfldata2$Points_FG_20_29

#Kickers Field Goals 30-39 yds
nfldata2$Points_FG_30_39 <- round(nfldata2$FG_30.39 * 3)
nfldata2$Points_FG_30_39

#Kickers Field Goals 40-49 yds
nfldata2$Points_FG_40_49 <- round(nfldata2$FG_40.49 * 4)
nfldata2$Points_FG_40_49

#Kickers Field Goals 50+ yds
nfldata2$Points_FG_50 <- round(nfldata2$FG_50. * 5)
nfldata2$Points_FG_50 

#Kickers Point After Attempt Made
nfldata2$Points_Pts_After_Att_Mde <- round(nfldata2$PAT_Made * 1)
nfldata2$Points_Pts_After_Att_Mde

#Defense Sacks
nfldata2$Points_Sack <-round(nfldata2$Sack * 1)
nfldata2$Points_Sack

#Defense Interception
nfldata2$Points_Def_Int <- round(nfldata2$Int.1)
nfldata2$Points_Def_Int

#Defense Fumble Recovery
nfldata2$Points_Fum_Rec <- nfldata2$Fum_Rec.1 * 2
nfldata2$Points_Fum_Rec

#Defense Touchdown
nfldata2$Points_Def_TD <- (nfldata2$Fum_TD.1 + nfldata2$Int_TD) * 6
nfldata2$Points_Def_TD

#Defense Safety
nfldata2$Points_Safety <- nfldata2$Saf.1 * 2
nfldata2$Points_Safety

#Blocked Kicks
nfldata2$Points_Blk_Kick <-nfldata2$Block * 2
nfldata2$Points_Blk_Kick

#Kickoff and Punt Return Touchdowns
nfldata2$Points_kck_rtrn_TD <- nfldata2$Return_TD.1 * 6
nfldata2$Points_kck_rtrn_TD

#Defense Points Allowed = 0
nfldata2$Points_pts_alwd_0 <- nfldata2$Pts_Allow_0 * 10
nfldata2$Points_pts_alwd_0

#Defense Points Allowed = 1-6
nfldata2$Points_pts_alwd_1_6 <- nfldata2$Pts_Allow_1.6 * 7
nfldata2$Points_pts_alwd_1_6

#Defense Points Allowed = 7-13
nfldata2$Points_pts_alwd_7_13 <- nfldata2$Pts_Allow_7.13 * 4
nfldata2$Points_pts_alwd_7_13

#Defense Points Allowed = 14-20
nfldata2$Points_pts_alwd_14_20 <- nfldata2$Pts_Allow_14.20 * 1
nfldata2$Points_pts_alwd_14_20

#Defense Points Allowed = 21-27
nfldata2$Points_pts_alwd_21_27 <- nfldata2$Pts_Allow_21.27 * 0
nfldata2$Points_pts_alwd_21_27

#Defense Points Allowed = 28-34
nfldata2$Points_pts_alwd_28_34 <- nfldata2$Pts_Allow_28.34 * -1
nfldata2$Points_pts_alwd_28_34

#Defense Points Allowed = 35+
nfldata2$Points_pts_alwd_35 <- nfldata2$Pts_Allowed_35. * -4
nfldata2$Points_pts_alwd_35 

#Defense Extra Point Returned
nfldata2$Points_Xtra_Pt_Rtrn <- nfldata2$Def_Player_2pt_Ret * 2
nfldata2$Points_Xtra_Pt_Rtrn

# Data Cleaning and Checking ----------------------------------------------

FF_Points <- names(nfldata2)
FF_Points <- subset(FF_Points, grepl("Points", FF_Points))
FF_Points

for (i in FF_Points) {
  val <- noquote(i)
  stat_frame <- subset(nfldata2, !is.na(val))
  count(stat_frame, 'position')
}
