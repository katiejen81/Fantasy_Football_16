<h1>Fantasy Football Collaboration Programs 2016 season</h1>
<br />
<p>This repo will host the shared programs used to retrieve and analyze data for the Fantasy Football league</p>
<p>Information about the Python Programs</p>
<ul>
	<li><u>nfldataretieval</u> Sorry for the misspelling - This uses the python package NFLGame to get schedules and statistics</li>
	<li><u>data_retrieval_from_api</u> - Uses the nfl.com api directly to get all of the statistics available on the site</li>
	<li>rank_retrieval_from_api - Uses the nfl.com api directly to get all of the editor draft ranks for the current season</li>
	<li>Undrafted_Player_Report - Aggregated total season points of undrafted players in the league, along with a week breakdown</li>
	<li>Team_Player_Report - Shows a trend of our team performance by week this season</li>
</ul>
<p>Information about the R Programs</p>
<ul>
    <li>Clean Up Data.r - This cleans up the full_stats file (there are duplicates in the file) and calculates the game level fantasy points for each player for each week in the seasons between 2013 and 2015</li>
</ul>
<p>Information about the data files</p>
<ul>
	<li>team_roster_week.csv - A report of our team players and their points by week</li>
	<li>undrafted_players.csv - A report of the top 100 undrafted players as of program runtime</li>
	<li>undrafted_player_week.csv - A report of the top 100 undrafted players points broken down by week as of program runtime</li>
	<li>full_stats.csv - Full week level game statistics for the 2013 - 2015 seasons</li>
	<li>rank_retrieval_from_api.csv - nfl.com editor draft rankings for the 2016 season</li>
	<li>Fantasy_Point_Values.csv - League point values for current season</li>
	<li>All Players.csv - Player lists and demographics. Haven't updated this in a while. If you need it run the code to update it</li>
	<li>Schedule since 2013.csv - Schedule information for the 2013 - 2015 seasons</li>
</ul>
