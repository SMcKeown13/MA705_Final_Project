# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 02:37:35 2020

@author: Sean
"""
import requests
import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import re

import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


#Preparing the play by play dataframe
armyO = pd.read_csv('armyO.csv')
armyO['lead_team'] = np.where(armyO['offense_score'] >= armyO['defense_score'], 'Lead', 'Losing')
armyO['lead_team'] = np.where(armyO['offense_score'] == armyO['defense_score'], 'Tie', armyO['lead_team'])
armyO['run_or_pass'] = np.where(armyO['play_type'].str.contains('Rush'), 'Run', 'None')
armyO['run_or_pass'] = np.where(armyO['play_type'].str.contains('Pass'), 'Pass', armyO['run_or_pass'])
armyO['converted'] = np.where(armyO['distance'] <= armyO['yards_gained'], 'Yes', 'No')
armyO['home_away'] = np.where(armyO['home'].str.contains('Army'), 'Home', 'Away')
armyGameDf = pd.read_csv('ArmyGameDf.csv')

#Preparing the game stats dataframe
armyGameDf = pd.read_csv('ArmyGameDf.csv')
armyGameDf = armyGameDf.loc[:, ~armyGameDf.columns.str.contains('^Unnamed')]
time = armyGameDf.possessionTime.str.findall('\d+')
time_of_Poss = []
for i in range(len(time)):
    if isinstance(time[i], list):
        mint = int(time[i][0]) * 60
        sec = int(time[i][1])
        totalTime = mint + sec
        time_of_Poss.append(totalTime)
    else:
        time_of_Poss.append(time[i])
armyGameDf['totalTime'] = time_of_Poss
armyGamesPlayed = armyGameDf[~armyGameDf.homeAway.str.contains('No_Game')]

#Preparing the ArmyDrive dataframe
armyDriveO = pd.read_csv('armyDriveO.csv')
minutes = armyDriveO['elapsed'].str.findall("'minutes': \d+")
armyDriveO['elapsed_minutes'] = minutes
seconds = armyDriveO['elapsed'].str.findall("'seconds': \d+")

full_min = []
for i in range(len(minutes)):
    full_min.append(re.findall('\d+', minutes[i][0]))
elap_min = []
for j in range(len(full_min)):
    time = int(full_min[j][0])
    elap_min.append(time*60)

full_sec = []
for i in range(len(minutes)):
    full_sec.append(re.findall('\d+', seconds[i][0]))
elap_sec = []
for j in range(len(full_sec)):
    time = int(full_sec[j][0])
    elap_sec.append(time)
    
elapsed_seconds = np.array(elap_sec)
elapsed_minutes = np.array(elap_min)
elapsed_time = elapsed_seconds + elapsed_minutes
armyDriveO['elapsed_time'] = elapsed_time
armyDriveO['scoring'] = armyDriveO['scoring'].replace({True: 'TRUE', False: 'FALSE'})


#Start of defining the app and its layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
        html.Div([html.H1("Army Football Offense under Jeff Monken (2014-2020)", style={'text-align':'center'}),
                  html.H6("Please select the years you would like to look at.", style={'text-align':'center'}),
                       dcc.RangeSlider( id = 'year_slider',
                            min=armyGamesPlayed['year'].min(),
                            max=armyGamesPlayed['year'].max(),
                            step=None,
                            marks={
                                2014: '2014',
                                2015: '2015',
                                2016: '2016',
                                2017: '2017',
                                2018: '2018', 
                                2019: '2019', 
                                2020: '2020'
                            },
                            value=[2014, 2020]
                        ),
                html.H6("Please select the weeks you would like to look at.", style={'text-align':'center'}),
                        dcc.RangeSlider( id = 'week_slider',
                            min=armyGamesPlayed['week'].min(),
                            max=armyGamesPlayed['week'].max(),
                            step=None,
                            marks={
                                1: 'Week 1',
                                2: 'Week 2',
                                3: 'Week 3',
                                4: 'Week 4',
                                5: 'Week 5', 
                                6: 'Week 6', 
                                7: 'Week 7',
                                8: 'Week 8',
                                9: 'Week 9',
                                10: 'Week 10', 
                                11: 'Week 11', 
                                12: 'Week 12',
                                13: 'Week 13',
                                14: 'Week 14',
                                15: 'Week 15',
                                16: 'Week 16',
                                17: 'Week 17',
                                18: 'Week 18'
                            },
                            value=[1, 16]
                        )
                    ]),
            html.Div([html.H3("Key Offensive Statistics", style={'text-align':'center'}),
                    html.Div(
                        [html.H6(id="total_yards_text"), html.P("Total yards per game")],
                        id="total_yards",
                        style={'text-align':'center'},
                        className="three columns"
                            ),  
                        html.Div(
                                [html.H6(id="pointsText"), html.P("Points per game")],
                                id="points",
                                style={'text-align':'center'},
                                className="three columns"
                            ),
                            html.Div(
                                [html.H6(id="turnoversText"), html.P("Turnovers per game")],
                                id="turnovers",
                                style={'text-align':'center'},
                                className="three columns"
                            ),
                            html.Div(
                                [html.H6(id="TOPText"), html.P("Time of Possession")],
                                id="Time_of_Poss",
                                style={'text-align':'center'},
                                className="three columns"
                            )
                            ],
                    className="twelve columns",
                ),
    html.Div([
        html.Div([
            dcc.Graph(id='rush_pass_yards')
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='rush_pass_play_yards')
        ], className="six columns"),
    ], className="row"),
    html.Div([
        html.Div([html.H3('Play Scenarios'),
                html.P("Filter by lead:"),
                dcc.Checklist(
                id='lead_checklist',                      
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in armyO['lead_team'].unique()
                ],
                value=['Lead','Losing','Tie'],    

                className='my_box_container',         
                # style={'display':'flex'},             

                inputClassName='my_box_input',          
                inputStyle={'cursor':'pointer'},      

                labelClassName='my_box_label',          
                labelStyle={'background':'#A5D6A7',   
                             'padding':'0.5rem 1rem',
                             'border-radius':'0.5rem'},

            ), 
                html.P("Filter by home or away:"),
                dcc.Checklist(
                id='location_checklist',                      
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in armyO['home_away'].unique()
                ],
                value=['Home','Away'],    

                className='my_box_container',                    

                inputClassName='my_box_input',          
                inputStyle={'cursor':'pointer'},      

                labelClassName='my_box_label',         
                labelStyle={'background':'#A5D6A7',   
                             'padding':'0.5rem 1rem',
                             'border-radius':'0.5rem'},

            ),
                html.P("Filter by yards to gain:"),
        dcc.RangeSlider(
            id='yard_to_gain_slider', 
            marks={
                0: {'label': '<1 yd', "style": {"transform": "rotate(45deg)"}},     
                2: {'label': '2 yd', "style": {"transform": "rotate(45deg)"}},
                4: {'label': '4 yd', "style": {"transform": "rotate(45deg)"}},
                6: {'label': '6 yd', "style": {"transform": "rotate(45deg)"}},
                8: {'label': '8 yd', "style": {"transform": "rotate(45deg)"}},
                10: {'label': '10 yd', "style": {"transform": "rotate(45deg)"}},
                15: {'label': '15 yd', "style": {"transform": "rotate(45deg)"}},
                20: {'label': '20 yd', "style": {"transform": "rotate(45deg)"}}
            },
            step= None,               
            min=0,
            max=20,
            value=[0,10],     
            dots=True,             
            ),
        html.P("Filter by yards until endzone:"),
        dcc.RangeSlider(
            id='yard_to_goal_slider',
            marks={
                0: {'label': '<1 yd'},
                20: {'label': '20 yds'},
                50: {'label': '50 yds'},
                80: {'label': '80 yds'},
                100: {'label': '100 yds'}
            },
            step= None,                
            min=0,
            max=armyO['yards_to_goal'].max(),
            value=[0,100], 
            dots=True,            
                )
        ], className = 'two columns'),
        html.Div([
            dcc.Graph(id='down_yards')
        ], className="five columns"),

        html.Div([
            dcc.Graph(id='down_selection')
        ], className="five columns"),
                
        html.Div([html.H3('Drive Scenarios'),
                html.P("Filter by scoring drive:"),
                dcc.Checklist(
                id='score_checklist',
                options=[
                                 {'label': 'Scoring Drive', 'value': 'TRUE'},
                                 {'label': 'Non Scoring Drive', 'value': 'FALSE'}
                ],
                value=['TRUE','FALSE'],   

                className='my_box_container',

                inputClassName='my_box_input',          
                inputStyle={'cursor':'pointer'},      

                labelClassName='my_box_label',         
                labelStyle={'background':'#A5D6A7',   
                             'border-radius':'0.5rem'},
            ), 
                html.P("Filter by quarter drive started:"),
                dcc.RangeSlider(
                    id='quarter_slider',
                    marks={
                        1: {'label': '1Q', "style": {"transform": "rotate(45deg)"}},
                        2: {'label': '2Q', "style": {"transform": "rotate(45deg)"}},
                        3: {'label': '3Q', "style": {"transform": "rotate(45deg)"}},
                        4: {'label': '4Q', "style": {"transform": "rotate(45deg)"}},
                        5: {'label': '1OT', "style": {"transform": "rotate(45deg)"}},
                        6: {'label': '2OT', "style": {"transform": "rotate(45deg)"}},
                    },
                    step= None,               
                    min=1,
                    max=6,
                    value=[0,4],     
                    dots=True,             
                    )
        ], className = 'two columns'),
        html.Div([
            dcc.Graph(id='drive_time')
        ], className="five columns"),
        html.Div([
            dcc.Graph(id='drive_play')
        ], className="five columns"),
    ], className="row")
]
)

    

@app.callback(
    Output('rush_pass_yards','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value')
)

def update_rush_pass_yards(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    dff = dff.groupby(["year"], as_index=False)['rushingYards', 'netPassingYards'].mean()
    
    
    bar_chart = go.Figure(go.Bar(x=dff['year'], y=dff["rushingYards"], 
                                 name='rushingYards', marker_color='rgb(0,0,0)'))
    bar_chart.add_trace(go.Bar(x=dff['year'], y=dff["netPassingYards"], 
                               name='netPassingYards', marker_color='rgb(212,175,55)'))

    
#    bar_chart.add_layout_image(
#        dict(
#            source="https://www.logolynx.com/images/logolynx/2d/2d1d83a93e3977179a56c9d865c8793b.png",
#            xref="paper", yref="paper",
#            x=1, y=1.05,
#            sizex=0.2, sizey=0.2,
#            xanchor="right", yanchor="bottom"
#        )
#)
    bar_chart.update_xaxes(type='category')
    
    bar_chart.update_layout(barmode='stack')
    
    bar_chart.update_layout(title='Pass v. Rush Per Game', xaxis_title="Year",
    yaxis_title="Yards Per Game")
    
    return (bar_chart)


@app.callback(
    Output('rush_pass_play_yards','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value')
)

def update_rush_pass_play_yards(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    dff = dff.groupby(["year"], as_index=False)['yardsPerRushAttempt', 'yardsPerPass'].mean()
    
    
    bar_chart = go.Figure()
    
    bar_chart.add_trace(go.Bar(name='yardsPerRushAttempt', x=dff['year'], y=dff['yardsPerRushAttempt'], 
           marker_color='rgb(0,0,0)'))
    bar_chart.add_trace(go.Bar(name='yardsPerPass', x=dff['year'], y=dff['yardsPerPass'], 
           marker_color='rgb(212,175,55)'))

    bar_chart.update_xaxes(type='category')

    bar_chart.update_layout(barmode='group')
    
    bar_chart.update_layout(title='Pass v. Rush Yds./Play', xaxis_title="Year",
    yaxis_title="Yards per Play")
    
#    bar_chart.add_layout_image(
#        dict(
#            source="ARMYLOGO.png",
#            xref="paper", yref="paper",
#            x=1, y=1.05,
#            sizex=0.2, sizey=0.2,
#            xanchor="right", yanchor="bottom"
#        )
#)
    
    return (bar_chart)
  
@app.callback(
    Output('down_yards','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value'),
    Input(component_id='lead_checklist', component_property='value'),
    Input(component_id='location_checklist', component_property='value'),
    Input(component_id='yard_to_gain_slider', component_property='value'),
    Input(component_id='yard_to_goal_slider', component_property='value')
)

def update_down_yards(years_chosen, weeks_chosen, lead_chosen, location_chosen, yards_to_gain, yards_to_goal):
    dff=armyO[(armyO['Year']>=years_chosen[0])&(armyO['Year']<=years_chosen[1])]
    dff = dff[(dff['Week']>=weeks_chosen[0])&(dff['Week']<=weeks_chosen[1])]
    dff = dff[(dff['down'] > 0) & (dff['down'] <= 4)]
    dff = dff[~dff.play_type.str.contains('Punt')]
    dff = dff[(dff['distance']>=yards_to_gain[0])&(dff['distance']<=yards_to_gain[1])]
    dff = dff[(dff['yards_to_goal']>=yards_to_goal[0])&(dff['yards_to_goal']<=yards_to_goal[1])]
    dff = dff[dff['lead_team'].isin(lead_chosen)]
    dff = dff[dff['home_away'].isin(location_chosen)]
    dff = dff.groupby(["down"], as_index=False)['distance', 'yards_gained'].mean()  

    bar_chart = go.Figure()
    
    bar_chart.add_trace(go.Bar(name='distance', x=dff["down"], y=dff['distance'], 
           marker_color='rgb(0,0,0)'))
    bar_chart.add_trace(go.Bar(name='yards_gained', x=dff["down"], y=dff['yards_gained'], 
           marker_color='rgb(212,175,55)'))

    bar_chart.update_xaxes(type='category')
    
    bar_chart.update_layout(barmode='group')
    
    bar_chart.update_layout(title='Down Performance Under Jeff Monken', xaxis_title="Down",
    yaxis_title="Yards")
    
    return (bar_chart)


@app.callback(
    Output('down_selection','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value'),
    Input(component_id='lead_checklist', component_property='value'),
    Input(component_id='location_checklist', component_property='value'),
    Input(component_id='yard_to_gain_slider', component_property='value'),
    Input(component_id='yard_to_goal_slider', component_property='value')
)

def update_down_selection(years_chosen, weeks_chosen, lead_chosen, location_chosen, yards_to_gain, yards_to_goal):
    dff=armyO[(armyO['Year']>=years_chosen[0])&(armyO['Year']<=years_chosen[1])]
    dff = dff[(dff['Week']>=weeks_chosen[0])&(dff['Week']<=weeks_chosen[1])]
    dff = dff[(dff['down'] > 0) & (dff['down'] <= 4)]
    dff = dff[~dff.play_type.str.contains('Punt')]
    dff = dff[dff['lead_team'].isin(lead_chosen)]
    dff = dff[dff['home_away'].isin(location_chosen)]
    dff = dff[(dff['distance']>=yards_to_gain[0])&(dff['distance']<=yards_to_gain[1])]
    dff = dff[(dff['yards_to_goal']>=yards_to_goal[0])&(dff['yards_to_goal']<=yards_to_goal[1])]
    dffrun = dff[dff['run_or_pass'] == 'Run']
    dffpass = dff[dff['run_or_pass'] == 'Pass']
    dff_run_plays = dffrun.groupby(["down"], as_index=False)['run_or_pass'].count()
    dff_pass_plays = dffpass.groupby(["down"], as_index=False)['run_or_pass'].count()

    bar_chart = go.Figure()
    
    bar_chart.add_trace(go.Bar(name='# of rush plays', x=dff_run_plays["down"], y=dff_run_plays['run_or_pass'], 
           marker_color='rgb(0,0,0)'))
    bar_chart.add_trace(go.Bar(name='# of pass plays', x=dff_pass_plays["down"], y=dff_pass_plays['run_or_pass'], 
           marker_color='rgb(212,175,55)'))

    bar_chart.update_xaxes(type='category')
    
    bar_chart.update_layout(barmode='stack')
    
    bar_chart.update_layout(title='Play Selection by down Under Jeff Monken', xaxis_title="Down",
    yaxis_title="# of plays run")
    
    return (bar_chart)



@app.callback(
    Output("total_yards_text", "children"),
    [
    Input('year_slider','value'),
    Input('week_slider', 'value')
    ],
)
def update_total_yards(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    avg = dff.totalYards.mean()
    return round(avg, 1)

@app.callback(
    Output("pointsText", "children"),
    [
    Input('year_slider','value'),
    Input('week_slider', 'value')
    ],
)
def update_points(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    avg = dff.points.mean()
    return round(avg, 1)

@app.callback(
    Output("turnoversText", "children"),
    [
    Input('year_slider','value'),
    Input('week_slider', 'value')
    ],
)
def update_turnovers(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    avg = dff.turnovers.mean()
    return round(avg, 1)

@app.callback(
    Output("TOPText", "children"),
    [
    Input('year_slider','value'),
    Input('week_slider', 'value')
    ],
)
def update_TOP(years_chosen, weeks_chosen):
    dff=armyGamesPlayed[(armyGamesPlayed['year']>=years_chosen[0])&(armyGamesPlayed['year']<=years_chosen[1])]
    dff = dff[(dff['week']>=weeks_chosen[0])&(dff['week']<=weeks_chosen[1])]
    avg = dff.totalTime.mean()
    minutes = avg // 60
    seconds = round(avg % 60, 1)
    return '{} minutes and {} seconds'.format(minutes, seconds)

@app.callback(
    Output('drive_time','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value'),
    Input(component_id='score_checklist', component_property='value'),
    Input(component_id='quarter_slider', component_property='value'),
)

def update_drive_time(years_chosen, weeks_chosen, scoring_chosen, quarter_chosen):
    dff=armyDriveO[(armyDriveO['Year']>=years_chosen[0])&(armyDriveO['Year']<=years_chosen[1])]
    dff = dff[(dff['Week']>=weeks_chosen[0])&(dff['Week']<=weeks_chosen[1])]
    dff = dff[dff['scoring'].isin(scoring_chosen)]
    dff = dff[(dff['start_period']>=quarter_chosen[0])&(dff['start_period']<=quarter_chosen[1])]
    dff = dff.groupby(["Year"], as_index=False)['plays'].mean()
    
    
    bar_chart = go.Figure()
    
    bar_chart.add_trace(go.Bar(name='# of plays', x=dff['Year'], y=dff['plays'], 
           marker_color='rgb(0,0,0)'))

    bar_chart.update_xaxes(type='category')

    
    bar_chart.update_layout(title='# of Plays per Drive', xaxis_title="Year",
    yaxis_title="# of Play")
    
#    bar_chart.add_layout_image(
#        dict(
#            source="ARMYLOGO.png",
#            xref="paper", yref="paper",
#            x=1, y=1.05,
#            sizex=0.2, sizey=0.2,
#            xanchor="right", yanchor="bottom"
#        )
#)
    
    return (bar_chart)


@app.callback(
    Output('drive_play','figure'),
    Input('year_slider','value'),
    Input('week_slider', 'value'),
    Input(component_id='score_checklist', component_property='value'),
    Input(component_id='quarter_slider', component_property='value'), 
)

def update_drive_play(years_chosen, weeks_chosen, scoring_chosen, quarter_chosen):
    dff=armyDriveO[(armyDriveO['Year']>=years_chosen[0])&(armyDriveO['Year']<=years_chosen[1])]
    dff = dff[(dff['Week']>=weeks_chosen[0])&(dff['Week']<=weeks_chosen[1])]
    dff = dff[dff['scoring'].isin(scoring_chosen)]
    dff = dff[(dff['start_period']>=quarter_chosen[0])&(dff['start_period']<=quarter_chosen[1])]
    dff = dff.groupby(["Year"], as_index=False)['elapsed_time'].mean()
    
    
    bar_chart = go.Figure()
    
    bar_chart.add_trace(go.Bar(name='elapsed_time', x=dff['Year'], y=dff['elapsed_time'], 
           marker_color='rgb(212,175,55)'))


    bar_chart.update_xaxes(type='category')

    
    bar_chart.update_layout(title='Time taken per Drive', xaxis_title="Year")
    
    bar_chart.update_layout(
        yaxis = dict(
        tickmode = 'array',
        tickvals = [0, 120, 240, 360, 480, 600, 720, 840, 960],
        ticktext = ['0 minutes', 'Two minutes', 'Four minutes', 
                    'Six minutes', 'Eight minutes', 'Ten minutes',
                    'Twelve minutes', 'Fourteen minutes', 'Sixteen minutes']
    )
)
    
#    bar_chart.add_layout_image(
#        dict(
#            source="ARMYLOGO.png",
#            xref="paper", yref="paper",
#            x=1, y=1.05,
#            sizex=0.2, sizey=0.2,
#            xanchor="right", yanchor="bottom"
#        )
#)
    
    return (bar_chart)








if __name__ == '__main__':
    app.run_server(debug=True)
    
    