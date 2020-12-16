# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 02:45:37 2020

@author: Sean
"""
"""
File used to get game stats
More complex separating JSON data and cleaning it
"""
import requests
import json
import pandas as pd

columns2 = ['id',
         'homeAway',
         'points',
         'yardsPerPass',
         'rushingYards',
         'netPassingYards',
         'totalYards',
         'completionAttempts',
         'totalPenaltiesYards',
         'firstDowns',
         'possessionTime',
         'yardsPerRushAttempt',
         'turnovers',
         'rushingAttempts',
         'fumblesLost',
         'interceptions',
         'thirdDownEff',
         'fourthDownEff',
         'passesDeflected',
         'qbHurries',
         'sacks',
         'tackles',
         'defensiveTDs',
         'tacklesForLoss',
         'totalFumbles',
         'fumblesRecovered',
         'kickingPoints',
         'kickReturns',
         'kickReturnTDs',
         'kickReturnYards',
         'passingTDs',
         'puntReturns',
         'puntReturnTDs',
         'puntReturnYards',
         'rushingTDs']
armyGameDf = pd.DataFrame(columns = columns2)

for i in range(2014, 2021):
    for w in range(1,19):
        try:
            url = "https://api.collegefootballdata.com/games/teams?year={}&week={}&seasonType=regular&team=Army".format(i, w)
            
            army_reqGame = requests.get(url)
            workGame = army_reqGame.raise_for_status()
            
            armyGame = army_reqGame.json()
            level1 = armyGame[0]
            armyL = []
            for k in range(2):
                armyL.append(['id', level1['id']])
                level2 = level1['teams'][k]
                if 'Army' in level2.values():
                    armyL.append(['homeAway', level2['homeAway']])
                    armyL.append(['points', level2['points']])
                    for j in range(len(level2['stats'])):
                        x, y = level2['stats'][j].values()
                        armyL.append([x, y])
            armyL.append(['year', i])
            armyL.append(['week', w])
            armyDict = dict(armyL)
            armyGameStats = pd.DataFrame([armyDict])
            armyGameDf = armyGameDf.append(armyGameStats)
        except IndexError:
            armyL = []
            armyL.append(['year', i])
            armyL.append(['week', w])
            armyL.append(['homeAway', 'No_Game'])
            armyDict = dict(armyL)
            armyGameStats = pd.DataFrame([armyDict])
            armyGameDf = armyGameDf.append(armyGameStats)
        
armyGameDf['thirdDownEff'] = armyGameDf['thirdDownEff'].astype(str)
armyGameDf['totalPenaltiesYards'] = armyGameDf['totalPenaltiesYards'].astype(str)
armyGameDf['possessionTime'] = armyGameDf['possessionTime'].astype(str)
armyGameDf['completionAttempts'] = armyGameDf['completionAttempts'].astype(str)
armyGameDf['fourthDownEff'] = armyGameDf['fourthDownEff'].astype(str)
armyGameDf.to_csv('ArmyGameDf.csv')  

armyGameDf           
                    

        








