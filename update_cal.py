from datetime import date
from moduls.fixtures import MatchFixtures

#Define season year 
today = date.today()
cur_year = today.year
cur_month = today.month

if cur_month < 8:
    season_year = cur_year - 1
else:
    season_year = cur_year

#Create instance of Matchfixtures
bvb = MatchFixtures(teamshort='Dortmund', year_season=season_year)

#Update calendar
bvb.make_ics()
