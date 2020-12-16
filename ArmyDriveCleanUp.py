# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 15:26:49 2020

@author: Sean
"""
"""
Filed used to practice cleaning the ArmyDriveDf to be used in app
"""
import numpy as np
import pandas as pd
import re

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



