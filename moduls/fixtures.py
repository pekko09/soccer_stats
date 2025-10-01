import requests as rq

class MatchFixtures:
    """A model to get all matches of a team id from openligadb API """

    def __init__(self, teamid, year_season):
        self.teamid = teamid
        self.year_season = year_season
        self.matches = []

    def get_matches(self, comp):
        """Method to call all matches of a team in a competition, given by comp"""
        
        #Check input
        if comp not in {'bl1', 'ucl', 'dfb'}:
            raise ValueError(f"Invalid input for parameter comp: {comp}. Please chose one of 'bl1', 'ucl', 'dfb'")

        #Define api url
        apiurl = f"https://api.openligadb.de/getmatchdata/{comp}/{self.year_season}"

        #Request data
        resp = rq.get(url=apiurl)
        if resp.status_code == 200:
            leaguefixtures = resp.json()
            for match in leaguefixtures:
                if match["team1"]["teamId"] == self.teamid or match["team2"]["teamId"] == self.teamid:
                    self.matches.append(match)

                    