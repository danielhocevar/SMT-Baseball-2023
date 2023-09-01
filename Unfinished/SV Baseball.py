import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
import xgboost as xgb
import curses, time
import matplotlib.patches as patches
import msvcrt
import ast
import math

ballpos = pd.read_excel(r'C:\Users\jaden\OneDrive - University of Toronto\UTSPAN\Carnegie Mellon\Data\SMT-Data-Challenge\smt_data_challenge_2023\ball_pos\ball_pos-1900_01_TeamKJ_TeamB.xlsx')
data = pd.read_excel(r'C:\Users\jaden\OneDrive - University of Toronto\UTSPAN\Carnegie Mellon\Data\SMT-Data-Challenge\smt_data_challenge_2023\player_pos\TeamB\player_pos-1900_TeamB\player_pos-1900_01_TeamKJ_TeamB.xlsx')
eventdata = pd.read_excel(r'C:\Users\jaden\OneDrive - University of Toronto\UTSPAN\Carnegie Mellon\Data\SMT-Data-Challenge\smt_data_challenge_2023\game_events\game_events-1900_01_TeamKJ_TeamB.xlsx')
datagroup = data.groupby('play_id').groups
events = []
data['timestamp'] = (np.ceil(data['timestamp']/30 + 0.5)*30).astype(int)
eventdata['timestamp'] = (np.ceil(eventdata['timestamp']/30 + 0.5)*30).astype(int)

ballpos['timestamp'] = (np.ceil(ballpos['timestamp']/30 + 0.5)*30).astype(int)
#print(ballpos['timestamp'])
for group in datagroup:
    #print(datagroup[group])
    #print(data.loc[datagroup[group],:])
    events += [data.loc[datagroup[group],:]]

dataadj = pd.DataFrame()
dataadj['game_id'] = ''
dataadj['play_id'] = ''
dataadj['timestamp'] = ''
dataadj['ballx'] = ''
dataadj['bally'] = ''
dataadj['ballz'] = ''
dataadj['player_position'] = ''
dataadj['event_code'] = ''
'''for i in range(16):
    dataadj[str(i + 1) + '_id'] = ''
    dataadj[str(i + 1) + '_Field_X'] = ''
    dataadj[str(i + 1) + '_Field_Y'] = '''''

dataadj['id'] = ''
dataadj['Field_X'] = ''
dataadj['Field_Y'] = ''




#print(len(dataadj.columns.tolist()))

for event in events:
    times = np.unique(event['timestamp'])

    for time in times:
        ind = event.index[event['timestamp'] == time].tolist()

        ballind = ballpos.index[ballpos['timestamp'] == time].tolist()
        #print(ballind)
        eventind = eventdata.index[eventdata['timestamp'] == time].tolist()
        #print(time,ballind,eventind)
        adj = [event.loc[ind[0], 'game_str'], event.loc[ind[0], 'play_id']]
        adj += [time]
        eventcodes = []
        playerpos = []
        for i in range(len(eventind)):
            playerpos += [eventdata.loc[eventind[i],'player_position']]
            eventcodes += [eventdata.loc[eventind[i],'event_code']]
        #print(ballind,time)
        if len(ballind) != 0:
            adj += [ballpos.loc[ballind[0],'ball_position_x'],ballpos.loc[ballind[0],'ball_position_y'],ballpos.loc[ballind[0],'ball_position_z']]
        else:
            adj += [np.nan,np.nan,np.nan]
        adj += [playerpos,eventcodes]
        inds = event.index[(event['timestamp'] == time)].tolist()
        positions = []
        x = []
        y = []
        for i in range(len(inds)):
            positions += [event.loc[inds[i],'player_position']]
            x += [event.loc[inds[i],'field_x']]
            y += [event.loc[inds[i],'field_y']]
        positions, x, y = zip(*sorted(zip(positions, x, y)))
        adj += [list(positions),list(x),list(y)]
        #print(len(adj))
        dataadj.loc[len(dataadj['game_id'])] = adj

writer = 'MLBgamev2' + '.xlsx'
dataadj.to_excel(writer)








