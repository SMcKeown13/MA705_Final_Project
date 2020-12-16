# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 04:05:25 2020

@author: Sean
"""
"""
Filed used to gather the data from the API and test code written before using 
on app
"""
import requests
import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import re

import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Used for web scraping and testing code

columns = ['id',
  'offense',
  'offense_conference',
  'defense',
  'defense_conference',
  'home',
  'away',
  'offense_score',
  'defense_score',
  'game_id',
  'drive_id',
  'drive_number',
  'play_number',
  'period',
  'clock' ,
  'offense_timeouts',
  'defense_timeouts',
  'yard_line',
  'yards_to_goal',
  'down',
  'distance',
  'scoring',
  'yards_gained',
  'play_type',
  'play_text',
  'ppa']
armyDf = pd.DataFrame(columns = columns)

columns1 = ["offense",
    "offense_conference",
    "defense",
    "defense_conference",
    "game_id",
    "id",
    "drive_number",
    "scoring",
    "start_period",
    "start_yardline",
    "start_yards_to_goal",
    "start_time",
#    "minutes",
#    "seconds",
    "end_period",
    "end_yardline",
    "end_yards_to_goal",
    "end_time",
#    "minutes",
#    "seconds",
    "elapsed",
#    "minutes",
#    "seconds",
    "plays",
    "yards",
    "drive_result"]
armyDriveDf = pd.DataFrame(columns = columns1)



#
#Will Get game info from 2014 til 2020
#for i in range(2014, 2021):
#    for w in range(1,16):
#        url = "https://api.collegefootballdata.com/games/teams?year={}&week={}&seasonType=regular&team=Army".format(i, w)
#        
#        army_reqGame = requests.get(url)
#        workGame = army_reqGame.raise_for_status()
#        
#        armyGame = army_reqGame.json()
#    
#        armyWeekGame = pd.DataFrame(armyGame, columns = columns1)
#        armyWeekGame['Year'] = i
#        armyWeekGame['Week'] = w
#        armyGameDf = armyGameDf.append(armyWeekGame)


#Will Get drive info from 2014 til 2019
#for i in range(2014, 2021):
#    for w in range(1,19):
#        url = "https://api.collegefootballdata.com/drives?seasonType=regular&year={}&week={}&team=Army".format(i, w)
#        
#        army_reqDrive = requests.get(url)
#        workDrive = army_reqDrive.raise_for_status()
#        
#        armyDrive = army_reqDrive.json()
#    
#        armyWeekDrive = pd.DataFrame(armyDrive, columns = columns1)
#        armyWeekDrive['Year'] = i
#        armyWeekDrive['Week'] = w
#        armyDriveDf = armyDriveDf.append(armyWeekDrive)
#
#armyDriveO = armyDriveDf[armyDriveDf['offense'] == 'Army']
#armyDriveO.to_csv("armyDriveO.csv")
#armyDriveO = pd.read_csv('armyDriveO.csv')


for i in range(2014, 2021):
    for w in range(1,19):
        url = "https://api.collegefootballdata.com/plays?seasonType=regular&year={}&week={}&team=Army".format(i, w)
        params = {}
        
        army_req = requests.get(url)
        work = army_req.raise_for_status()
        
        army = army_req.json()

        armyWeek = pd.DataFrame(army, columns = columns)
        armyWeek['Year'] = i
        armyWeek['Week'] = w
        armyDf = armyDf.append(armyWeek)
        
armyO = armyDf[armyDf['offense'] == 'Army']
armyO.to_csv("armyO.csv")
#armyO = pd.read_csv('armyO.csv')
#armyO['lead_team'] = np.where(armyO['offense_score'] >= armyO['defense_score'], 'Lead', 'Losing')
#armyO['lead_team'] = np.where(armyO['offense_score'] == armyO['defense_score'], 'Tie', armyO['lead_team'])
#armyO['converted'] = np.where(armyO['distance'] <= armyO['yards_gained'], 'Yes', 'No')
#
#
#
#avg = armyO.loc[armyO['offense'] == 'Army','yards_gained'].mean()
#
#rush = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'] == 'Rush'), 'yards_gained'].mean()
#rushStd = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'] == 'Rush'), 'yards_gained'].std()
#rushDf = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'] == 'Rush'), ['yards_gained','down','distance']]
#rushDf.reset_index(drop = True, inplace=True)
#passO = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'].str.contains('Pass', na=False)), 'yards_gained'].mean()
#passStd = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'].str.contains('Pass', na=False)), 'yards_gained'].std()
#passDf = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'].str.contains('Pass', na=False)), ['yards_gained','down','distance']]
#passDf.reset_index(drop = True, inplace=True)
#rush_distrbs = stats.norm(rush, rushStd)
#sim_rush_result = rush_distrbs.rvs()
#
#pass_distrbs = stats.norm(passO, passStd)
#sim_pass_result = pass_distrbs.rvs()
#
#downToGo = armyO.groupby('down')['distance'].mean()
#fumble = armyO.loc[(armyO['offense'] == 'Army') & (armyO['play_type'].str.contains('Fumble', na=False)), 'yards_gained'].sum()
#downToGoResult = armyO.groupby('down')['yards_gained'].mean()
#rushDownResult = rushDf.groupby('down')['yards_gained'].mean()
#rushDownDistance = rushDf.groupby('down')['distance'].mean()
#passDownResult = passDf.groupby('down')['yards_gained'].mean()
#passDownDistance = passDf.groupby('down')['distance'].mean()

#print(rushDf)
#print(passDf)

#rushDistribution = plt.hist(x = rushDf['yards_gained'], bins = 20)
#passDistribution = plt.hist(x = passDf['yards_gained'], bins = 20)
#rushDownResult.plot()

#Ideas for charts and types of charts
"""
Title: ARMY OFFENSE UNDER JEFF MONKEN(2014-2020)

Selection for all data based off a slider for years
Second Slider for all data based off week number
Both sliders should be two sided
After these two sliders put a statement saying something like, "X number of 
    offensive plays run for selection"


Can do all analysis with the x values being year to see change in tendencies

FInd total offensive yards per game average over course of week and year selection

Provide various game situations to select from and display play selection (run v pass).
    Type of scenarios to choose from, down, distance as less than or equal
    (i.e. if 5 is selected interpret as five or less to gain), leading or not,
    quarter, goal line with same interpretation as distance, home v away
    
Plot based off yards per type of play with same criteria as above

Plot based off same criteria average yards to go for various downs and success of conversion

Plot based off fourth down decisions and success

Plot based off of turnovers

Plot based off opponent and game data from games against those opponents
    i.e. Run v Pass vs NAVY and average yards gained
    
Plot how long in plays and elapsed time the drives were on average across years
"""


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
#app.layout = html.Div([
#    html.H1("Army Football Offense Analysis under Jeff Monken (2014-2020)", style={'text-align':'center'}),
#    html.Div([
#        dcc.RangeSlider(
#            min=armyO['Year'].min(),
#            max=armyO['Year'].max(),
#            step=None,
#            marks={
#                2014: '2014',
#                2015: '2015',
#                2016: '2016',
#                2017: '2017',
#                2018: '2018', 
#                2019: '2019', 
#                2020: '2020'
#            },
#            value=[2014, 2020]
#        ), 
#        dcc.RangeSlider(
#            min=armyO['Week'].min(),
#            max=armyO['Week'].max(),
#            step=None,
#            marks={
#                1: 'Week 1',
#                2: 'Week 2',
#                3: 'Week 3',
#                4: 'Week 4',
#                5: 'Week 5', 
#                6: 'Week 6', 
#                7: 'Week 7',
#                8: 'Week 8',
#                9: 'Week 9',
#                10: 'Week 10', 
#                11: 'Week 11', 
#                12: 'Week 12',
#                13: 'Week 13',
#                14: 'Week 14',
#                15: 'Week 15',
#                16: 'Week 16'
#            },
#            value=[1, 16]
#        )
#    ])
#])
#
#
#
#if __name__ == '__main__':
#    app.run_server(debug=True)

#armyGameDf = pd.read_csv('ArmyGameDf.csv')
#armyGameDf = armyGameDf.loc[:, ~armyGameDf.columns.str.contains('^Unnamed')]
#time = armyGameDf.possessionTime.str.findall('\d+')
#time_of_Poss = []
#for i in range(len(time)):
#    if isinstance(time[i], list):
#        mint = int(time[i][0]) * 60
#        sec = int(time[i][1])
#        totalTime = mint + sec
#        time_of_Poss.append(totalTime)
#    else:
#        time_of_Poss.append(time[i])
#armyGameDf['totalTime'] = time_of_Poss
#armyGamesPlayed = armyGameDf[~armyGameDf.homeAway.str.contains('No_Game')]

        

#dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
#dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]

#armyO['run_or_pass'] = np.where(armyO['play_type'].str.contains('Rush'), 'Run', 'None')
#armyO['run_or_pass'] = np.where(armyO['play_type'].str.contains('Pass'), 'Pass', armyO['run_or_pass'])
#dffrun = armyO[armyO['run_or_pass'] == 'Run']
#dff_run_plays = dffrun.groupby(["down"], as_index=False)['run_or_pass'].count()
#dff_run_yards = dffrun.groupby(["down"], as_index=False)['yards_gained'].mean()
#group = armyO.groupby(["down"], as_index=False)['run_or_pass' == 'Run'].count()














