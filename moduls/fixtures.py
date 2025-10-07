import requests as rq

class MatchFixtures:
    """A model to get all matches of a team id from openligadb API """

    def __init__(self, teamshort, year_season):
        self.teamshort = teamshort
        self.team_name = ''
        self.year_season = year_season
        self.teamid = self.get_teamid()
        self.matches = []
    
    def query_api(self, ep):
        """Method to query data from API of openligadb"""

        api_main = 'https://api.openligadb.de'
        api_url = f"{api_main}{ep}"
        try:
            #start query timeout 3s connect, 10s response max time
            resp = rq.get(url=api_url, timeout=(3,10))
            resp.raise_for_status()
            return resp.json()
        except rq.exceptions.HTTPError as e:
            print("HTTP-Fehler:", e)
            return []
        except rq.exceptions.RequestException as e:
            print("Allgemeiner Request-Fehler:", e)
            return []

    def get_teamid(self):
        """Method to get teamID from team short name"""

        #Check input
        api_ep = f"/getavailableteams/bl1/{self.year_season}"
        teams = self.query_api(ep=api_ep)
        available_teams = []

        for t in teams:
            available_teams.append(t['shortName'])
        
        if self.teamshort not in available_teams:
            raise ValueError(
                f"Invalid team '{self.teamshort}'. Choose one of:\n" + "\n".join(available_teams)
                )
        
        #Select team
        team = next(team for team in teams if team['shortName'] == self.teamshort)

        #Get team name
        self.team_name = team['teamName']

        #Get teamId
        return team['teamId']
        
    def get_matches(self, comp):
        """Method to call all matches of a team in a competition, given by comp"""
        
        #Check input
        if comp not in {'bl1', 'ucl', 'dfb', 'uel'}:
            raise ValueError(f"Invalid input for parameter comp: {comp}. Please chose one of 'bl1', 'ucl', 'dfb' or 'uel'")

        #Define competition labels
        comp_labels = {'bl1': 'BL', 'ucl': 'CL', 'dfb': 'DFB', 'uel': 'EL'}

        #Count items in list matches
        len_old = len(self.matches)

        #Request data
        apiep = f"/getmatchdata/{comp}/{self.year_season}"
        leaguefixtures = self.query_api(ep=apiep)
        
        if leaguefixtures:
            for match in leaguefixtures:
                if match["team1"]["teamId"] == self.teamid or match["team2"]["teamId"] == self.teamid:
                    self.matches.append(match)
            #Sort matches by date
            self.matches.sort(key=lambda x: x['matchDateTime'])
            #Calculate new matches added
            len_new = len(self.matches) - len_old
            print(f"{len_new} new matches found for team {self.team_name} in campaign {comp_labels[comp]}")
        else:
            print(f"0 new matches found for team {self.team_name} in campaign {comp_labels[comp]}") 


                    