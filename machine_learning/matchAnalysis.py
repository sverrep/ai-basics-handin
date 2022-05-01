import requests
import pandas as pd
import joblib
import json

def sanitizeMatch(response):
    if response['dire_score'] == 0 and response['radiant_score'] == 0:
        return False
    else:
        matchdata = {
            'match_id': response['match_id'], 
            'dire_score': response['dire_score'], 
            'radiant_score': response['radiant_score'], 
            'duration': response['duration'], 
            'radiant_win': response['radiant_win'], 
            'players': [] 
        }
        playerdata = []
        for player in response['players']:
            playerdata.append(sanitizePlayer(player))
        
        return matchdata, playerdata

def sanitizePlayer(player):
    playerdata = {
        'match_id': player['match_id'], 
        'hero_id': player['hero_id'], 
        'lane_role': player["lane_role"], 
        'lane': player['lane'], 
        'kills': player['kills'], 
        'deaths': player['deaths'], 
        'assists': player['assists'], 
        'hero_damage': player['hero_damage'], 
        'camps_stacked': player['camps_stacked'], 
        'gpm': player['gold_per_min'], 
        'hero_healing': player['hero_healing'], 
        'last_hits': player['last_hits'],  
        'net_worth': player['net_worth'],
        'obs_placed': player['obs_placed'],
        'obs_killed': player['observer_kills'],
        'sen_placed': player['sen_placed'],
        'tower_damage': player['tower_damage'],
        'xpm': player['xp_per_min'],
        'is_radiant': player['isRadiant'],
        'win': player['win'],
        'duration': player['duration'],
        'ml_lane_role': 0,
    }
    return playerdata

def getPlayerHero(player):
    with open("constants/heroes.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
        heroid = player['hero_id']
        hero_name = jsonObject[str(heroid)]['localized_name']
        return hero_name

def getPlayerData(players):
    player_data = []
    for player in players:
        findRole(player)
        hero_name = getPlayerHero(player)
        predicted_win = getPredictedWin(player)
        player_data.append({
            'hero_name': hero_name,
            'kills': player['kills'],
            'deaths': player['deaths'],
            'ml_lane_role': player['ml_lane_role'],
            'net_worth': player['net_worth'],
            'predicted_win': predicted_win,
            'win': player['win'],
        })
    return player_data

def displayData(data, query):
    players = getPlayerData(data[1])
    for idx, player in enumerate(players):
        if player['win'] == True:
            print("--------")
            print("Player ", idx+1, " played as: ", player['hero_name'], " and had ", player['kills'], " kills with ", player['deaths'], " deaths.")
            print("The ML model core_model thinks they played as a ", player['ml_lane_role'], ".")
            print("The win prediction model gave this player a ", player['predicted_win'], " chance of winning the game based on their performance, and they did.")
            print("--------")
        else:
            print("--------")
            print("Player ", idx+1, " played as: ", player['hero_name'], " and had ", player['kills'], " kills with ", player['deaths'], " deaths.")
            print("The ML model core_model thinks they played as a ", player['ml_lane_role'], ".")
            print("The win prediction model gave this player a ", player['predicted_win'], " chance of winning the game based on their performance, and they ended up losing.")
            print("--------")

def findRole(player):
    X = [[player['last_hits'], player['obs_placed'], player['gpm']]]
    df = pd.DataFrame(X)
    scaledX = loaded_scaler.transform(df)
    role = findCore(scaledX, player['lane_role'])
    player['ml_lane_role'] = role

def findCore(scaledX, laneRole):
    y = core_model.predict(scaledX)
    if y == 1:
        if laneRole == 1:
            return 1
        elif laneRole == 2:
            return 2
        elif laneRole == 3:
            return 3
    else:
        if laneRole == 1:
            return 5
        elif laneRole == 2:
            return 4
        elif laneRole == 3:
            return 4

def predictCoreWin(win_model, player):
    X = [[player['kills'], player['deaths'], player['assists'], player['gpm'], player['xpm'], player['duration']]]
    y = win_model.predict_proba(X)
    win = y[0][1]
    return win

def predictSoftSupWin(win_model, player):
    X = [[player['kills'], player['deaths'], player['assists'], player['gpm'], player['xpm'], player['duration'], player['obs_placed'], player['obs_killed']]]
    y = win_model.predict_proba(X)
    win = y[0][1]
    return win

def predictHardSupWin(win_model, player):
    X = [[player['kills'], player['assists'], player['gpm'], player['xpm'], player['duration'], player['obs_placed'], player['obs_killed']]]
    y = win_model.predict_proba(X)
    win = y[0][1]
    return win

def getPredictedWin(player):
    if player['ml_lane_role'] == 1:
        win_model = joblib.load("models/carry_win.sav")
        win = predictCoreWin(win_model, player)
    elif player['ml_lane_role'] == 2:
        win_model = joblib.load("models/mid_win.sav")
        win = predictCoreWin(win_model, player)
    elif player['ml_lane_role'] == 3:
        win_model = joblib.load("models/off_win.sav")
        win = predictCoreWin(win_model, player)
    elif player['ml_lane_role'] == 4:
        win_model = joblib.load("models/softsup_win.sav")
        win = predictSoftSupWin(win_model, player)
    elif player['ml_lane_role'] == 5:
        win_model = joblib.load("models/hardsup_win.sav")
        win = predictHardSupWin(win_model, player)

    return win
    


query = input("Enter your match ID: ")

response = requests.get(f'https://api.opendota.com/api/matches/{query}').json()
core_model = joblib.load("models/core_model.sav")
loaded_scaler = joblib.load("models/core_scaler.sav")
data = sanitizeMatch(response)

if data != False:
    displayData(data, query)