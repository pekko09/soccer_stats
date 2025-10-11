import requests as rq
from ics import Calendar, Event
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import hashlib

class APIClient:
    """Base class for API requests"""

    API_CONFIG = {
        'oldb': {
            'base_url': 'https://api.openligadb.de',
            'auth_type': 'none'
        },
        'kb': {
            'base_url': 'https://api.kickbase.com/v4',
            'auth_type': 'bearer' #?
        }
        }
    
    def _build_headers(self):
        """Create headers for API requests based on authentification type"""
        if self.auth_type == "bearer" and self.credential:
            return {"Authorization": f"Bearer {self.credential}"}
        elif self.auth_type == "apikey" and self.credential:
            return {"X-API-Key": self.credential}
        else:
            return {}  # no authentification
        
    def query_api(self, ep: str, api_choice: str = 'oldb', params: dict | None = None):
        """Method to query data from an API listed in dict API_CONFIG"""
        #Check input of api_choice
        if api_choice not in self.API_CONFIG:
            raise ValueError(f"Invalid base url selection '{api_choice}'. Choose one of: {list(self.API_CONFIG)}")
        
        #Set base url
        self.base_url = self.API_CONFIG[api_choice]['base_url']
        
        #Set auth type
        self.auth_type = self.API_CONFIG[api_choice]['auth_type']  
        #Create api url with endpoint
        api_url = f"{self.base_url}{ep}"

        try:
            #start query timeout 3s connect, 10s response max time
            headers = self._build_headers()
            resp = rq.get(url=api_url, headers=headers, params=params, timeout=(3,10))
            resp.raise_for_status()
            return resp.json()
        except rq.exceptions.HTTPError as e:
            print("HTTP-Fehler:", e)
            return []
        except rq.exceptions.RequestException as e:
            print("Allgemeiner Request-Fehler:", e)
            return []


class MatchFixtures(APIClient):
    """A model to get all matches of a team id from openligadb API """

    #Define competition labels
    COMP_NAMES = {'bl1': 'BL', 'ucl': 'CL', 'dfb': 'DFB-Pokal', 'uel': 'EL'}

    def __init__(self, teamshort: str, year_season: int):
        self.teamshort = teamshort
        self.team_name = ''
        self.year_season = year_season
        self.teamid = self.get_teamid()
        self.matches = []
        self.get_all_matches()

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
        
    def get_matches(self, comp: str):
        """Method to call all matches of a team in a competition, given by comp"""
        
        #Check input
        if comp not in self.COMP_NAMES:
            raise ValueError(f"Invalid input for parameter comp: {comp}. Please chose one of: {list(self.COMP_NAMES)}")

        #Init counter for matches
        match_counter = 0

        #Request data
        apiep = f"/getmatchdata/{comp}/{self.year_season}"
        leaguefixtures = self.query_api(ep=apiep)
        
        if leaguefixtures:
            for match in leaguefixtures:
                if match["team1"]["teamId"] == self.teamid or match["team2"]["teamId"] == self.teamid:
                    self.matches.append(match)
                    match_counter += 1
            #Sort matches by date
            self.matches.sort(key=lambda x: x['matchDateTime'])
            #Calculate new matches added
            print(f"{match_counter} new matches found for team {self.team_name} in campaign {self.COMP_NAMES[comp]}")
        else:
            print(f"0 new matches found for team {self.team_name} in campaign {self.COMP_NAMES[comp]}")
    
    def get_all_matches(self):
        """Method to get all matches of all running competitions"""

        # Define competitions
        for c in self.COMP_NAMES:
            self.get_matches(comp=c)
    
    
    def make_ics(self):
        """Method to create a ics calendar in github pages of repo soccer_stats"""
        #create calendar
        cal = Calendar()

        #Create events
        for match in self.matches:
            comp = self.COMP_NAMES[match['leagueShortcut']]
            home = match['team1']['teamName']
            away = match['team2']['teamName']
            start_date_utc = datetime.strptime(match['matchDateTimeUTC'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
            start_date_local = start_date_utc.astimezone(ZoneInfo("Europe/Berlin"))
            counter = f"Match {match['group']['groupOrderID']}:"

            #create deterministic uid
            uid_str = f"{comp}-{home}-{away}-{counter}"
            uid_hash = hashlib.md5(uid_str.encode('utf-8')).hexdigest()

            #create deterministic datetimestamp
            dt_clean = start_date_local.replace(second=0, microsecond=0)

            event = Event()
            event.name = f"{comp} {counter} {home} - {away}"
            event.begin = start_date_local
            event.end = start_date_local + timedelta(minutes=90)
            event.uid = f"{uid_hash}@soccer_stats"
            event.created = dt_clean
            event.last_modified = dt_clean

            cal.events.add(event)
        
        #Sort events
        cal.events = set(sorted(cal.events, key=lambda e: e.begin))

        #Write calendar file
        with open("docs/bvb_fixtures.ics", "w", encoding="utf-8") as f:
            f.writelines(cal.serialize_iter())



                    