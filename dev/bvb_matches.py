# Query all matches of current season in Bundesliga
import requests

#Define URL
teamid = 7 #BVB
league = 'bl1'
year = '2025'
apiurl = f"https://api.openligadb.de/getmatchdata/{league}/{year}"

#Response
response = requests.get(url=apiurl)

if response.status_code == 200:
    leaguefixtures = response.json()
    for match in leaguefixtures:
        if match["team1"]["teamId"] == teamid or match["team2"]["teamId"] == teamid:
            home = match["team1"]["teamName"]
            away = match["team2"]["teamName"]
            date = match["matchDateTime"]
            
            result = match["matchResults"]
            #Get full time result
            if result:
                ftr =  next((r for r in result if r['resultTypeID'] == 2), None)
                score = f"{ftr['pointsTeam1']} : {ftr['pointsTeam2']}"
            else:
                score = '- : -'
            # dict bauen
            loca = match.get('location')
        
            print(f"{date}  {loca}:  {home} - {away}  {score}")
else:
    print("Error in request")