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

data = pd.read_excel(r'C:\Users\jaden\OneDrive - University of Toronto\Sports Analytics\Python\MLBgamev4.xlsx')
gameinf = pd.read_excel(r'C:\Users\jaden\OneDrive - University of Toronto\UTSPAN\Carnegie Mellon\Data\SMT-Data-Challenge\smt_data_challenge_2023\game_info\game_info-1903_13_TeamNG_TeamA3.xlsx')
data['runners'] = ''
data['eventlist'] = ''
data['playersinplays'] = ''
percent = 0.95
firstx = 63.5
firsty = 63.5
secondx = 0
secondy = 131.1
thirdx = -1*63.5
thirdy = 63.5
fourthx = 0
fourthy = 0
data['outathome'] = ''
data['runscored'] = ''



for play in np.unique(data['play_id']):
    #print(play)
    events = []
    runner = []
    player_pos = []
    for time in data[play == data['play_id']]['timestamp']:
        inds = data.index[(play == data['play_id']) & (data['timestamp'] == time)].tolist()

        #print(inds)
        #print(eval(data.loc[inds[0],'event_code']))
        events += eval(data.loc[inds[0],'event_code'])
        player_pos += eval(data.loc[inds[0],'player_position'])

    if 4 in events:
        #print(10)
        tenx = []
        teny = []
        elevenx = []
        eleveny = []
        twelvex = []
        twelvey = []
        thirteenx = []
        thirteeny = []
        ballhit = events.index(4)
        for time in data[play == data['play_id']]['timestamp']:
            inds = data.index[(data['timestamp'] == time)].tolist()
            if 10 in eval(data.loc[inds[0],'id']):
                #print("yo")
                tenind = eval(data.loc[inds[0],'id']).index(10)
                tenx += [eval(data.loc[inds[0],'Field_X'])[tenind]]
                teny += [eval(data.loc[inds[0],'Field_Y'])[tenind]]
            if 11 in eval(data.loc[inds[0],'id']):
                elevenind = eval(data.loc[inds[0],'id']).index(11)
                elevenx += [eval(data.loc[inds[0],'Field_X'])[elevenind]]
                eleveny += [eval(data.loc[inds[0],'Field_Y'])[elevenind]]
            if 12 in eval(data.loc[inds[0],'id']):
                twelveind = eval(data.loc[inds[0],'id']).index(12)
                twelvex += [eval(data.loc[inds[0],'Field_X'])[twelveind]]
                twelvey += [eval(data.loc[inds[0],'Field_Y'])[twelveind]]
            if 13 in eval(data.loc[inds[0],'id']):
                thirteenind = eval(data.loc[inds[0],'id']).index(13)
                thirteenx += [eval(data.loc[inds[0],'Field_X'])[thirteenind]]
                thirteeny += [eval(data.loc[inds[0],'Field_Y'])[thirteenind]]
        length = len(tenx[ballhit:])
        i = ballhit
        if length != 0:
            dist1 = ((firstx - tenx[len(tenx) - 1])**2 + (firsty - teny[len(teny) - 1])**2)**0.5
            dist2 = ((secondx - tenx[len(tenx) - 1])**2 + (secondy - teny[len(teny) - 1])**2)**0.5
            dist3 = ((thirdx - tenx[len(tenx) - 1])**2 + (thirdy - teny[len(teny) - 1])**2)**0.5
            dist4 = ((fourthx - tenx[len(tenx) - 1])**2 + (fourthy - teny[len(teny) - 1])**2)**0.5
            runner += [np.where([dist1,dist2,dist3,dist4] == np.min([dist1,dist2,dist3,dist4]))[0][0] + 1]
        else:
            runner += [-1]

        length = len(elevenx[ballhit:])
        if length != 0:
            dist1 = ((firstx - elevenx[len(elevenx) - 1]) ** 2 + (firsty - eleveny[len(eleveny) - 1]) ** 2) ** 0.5
            dist2 = ((secondx - elevenx[len(elevenx) - 1]) ** 2 + (secondy - eleveny[len(eleveny) - 1]) ** 2) ** 0.5
            dist3 = ((thirdx - elevenx[len(elevenx) - 1]) ** 2 + (thirdy - eleveny[len(eleveny) - 1]) ** 2) ** 0.5
            dist4 = ((fourthx - elevenx[len(elevenx) - 1]) ** 2 + (fourthy - eleveny[len(eleveny) - 1]) ** 2) ** 0.5
            runner += [np.where([dist1,dist2,dist3,dist4] == np.min([dist1,dist2,dist3,dist4]))[0][0] + 1]
        else:
            runner += [-1]
        length = len(twelvex[ballhit:])

        if length != 0:
            dist2 = ((secondx - twelvex[len(twelvex) - 1]) ** 2 + (secondy - twelvey[len(twelvey) - 1]) ** 2) ** 0.5
            dist3 = ((thirdx - twelvex[len(twelvex) - 1]) ** 2 + (thirdy - twelvey[len(twelvey) - 1]) ** 2) ** 0.5
            dist4 = ((fourthx - twelvex[len(twelvex) - 1]) ** 2 + (fourthy - twelvey[len(twelvey) - 1]) ** 2) ** 0.5
            runner += [np.where([dist2, dist3, dist4] == np.min([dist2, dist3, dist4]))[0][0] + 2]

        else:
            runner += [-1]
        length = len(thirteenx[ballhit:])

        if length != 0:
            dist3 = ((thirdx - thirteenx[len(thirteenx) - 1]) ** 2 + (thirdy - thirteeny[len(thirteeny) - 1]) ** 2) ** 0.5
            dist4 = ((fourthx - thirteenx[len(thirteenx) - 1]) ** 2 + (fourthy - thirteeny[len(thirteeny) - 1]) ** 2) ** 0.5
            runner += [np.where([dist3, dist4] == np.min([dist3, dist4]))[0][0] + 3]
        else:
            runner  += [-1]
    ind = data.index[data['play_id'] == play].tolist()
    #print(ind[0],runner)
    data.loc[ind[0],'runners'] = str(runner)
    data.loc[ind[0],'eventlist'] = str(events)
    data.loc[ind[0],'playersinplays'] = str(player_pos)
    # iterate to check for outs at home
    outathome = 0
    runs = 0
    ind = data.index[data['play_id'] == play].tolist()[0]
    #print(play)
    #print(2 in ast.literal_eval(data.loc[ind,'playersinplays']))
    #print(data.loc[ind,'playersinplays'])
    #print(4 in runner and 2 in ast.literal_eval(data.loc[ind,'playersinplays']))
    if 11 in events:

        runs += 1
        if 11 in ast.literal_eval(data.loc[ind, 'id']):
            runs += 1
        if 12 in ast.literal_eval(data.loc[ind, 'id']):
            runs += 1
        if 13 in ast.literal_eval(data.loc[ind, 'id']):
            runs += 1
    elif 2 in ast.literal_eval(data.loc[ind,'playersinplays'])[2:] and (4 in runner[1:]) and 11 not in events:

        time = data.index[data['play_id'] == play].tolist()
        #print(time)
        for t in time:
            if 2 in ast.literal_eval(data.loc[t,'player_position'])[:]:
                time2 = t
        #print(time2)
        runners = ast.literal_eval(data.loc[ind,'runners'])
        #print(runners)
        #print(play,runners)
        #if runners != []:

            #print(4 in runners)
        i = 0

        for ran in runners:
            i += 1
            #print(play)
            if ran == 4:
                run = data.index[(data['play_id'] == play)].tolist()
                for r in run:
                    if i + 9 in ast.literal_eval(data.loc[r,'id']):
                        rprime = r

                #print(run)
                if not (data.loc[rprime,'timestamp'] < time2):
                    print('yo')
                    outathome += 1
                else:
                    print('yo')
                    runs += 1
    else:
        if 4 in runner[2:]:
            print(play)

            runs += 1
    #print(play,runs)



    data.loc[ind,'outathome'] = outathome
    data.loc[ind,'runscored'] = runs
data['otherouts'] = ''
data['strikeouts'] = ''
plays = len(np.unique(data['play_id']))
for play in np.unique(data['play_id']):
    otherouts = 0
    strikeouts = 0
    #print(play)
    index = gameinf.index[gameinf['play_per_game'] == play].tolist()
    prev = []

    if play != 1 and len(index) == 1:
        prev = gameinf.index[gameinf['play_per_game'] == play - 1].tolist()
    if play != 1 and play != plays and len(prev) == 1 and prev[0] != 0:
        #print((gameinf.loc[index, 'inning'], gameinf.loc[prev, 'inning']),gameinf.loc[index, 'top_bottom_inning'].values, gameinf.loc[prev, 'top_bottom_inning'].values)
        if (gameinf.loc[index, 'inning'].values == gameinf.loc[prev, 'inning'].values) and (gameinf.loc[index, 'top_bottom_inning'].values == gameinf.loc[prev, 'top_bottom_inning'].values) and gameinf.loc[index, 'inning'].values < 10:
            ind = data.index[data['play_id'] == play - 1].tolist()[0]
            #print(ind)
            runners = ast.literal_eval(data.loc[ind, 'runners'])
            i = 0
            yo = data.index[data['play_id'] == play].tolist()[0]
            if gameinf.loc[prev[0] - 1, 'batter'] == gameinf.loc[prev, 'batter'].values[0] and gameinf.loc[prev, 'batter'].values[0] not in [gameinf.loc[index, 'batter'].values[0],
                                                                  gameinf.loc[index, 'first_baserunner'].values[0],
                                                                  gameinf.loc[index, 'second_baserunner'].values[0],
                                                                  gameinf.loc[index, 'third_baserunner'].values[0]]:
                for runner in runners:
                    i += 1
                    if runner == 1:
                        if  (11 not in ast.literal_eval(data.loc[yo,'id'])):
                            #print(play)
                            otherouts += 1
                    elif runner == 2:
                        #print(data.loc[yo,'playersinplays'])
                        if (12 not in ast.literal_eval(data.loc[yo,'id'])):
                            otherouts += 1
                    elif runner == 3:
                        if (13 not in ast.literal_eval(data.loc[yo,'id'])):
                            otherouts += 1
            if ast.literal_eval(data.loc[ind,'eventlist']) == [1,4,2,5] and otherouts == 0:

                otherouts += 1
            if prev[0] != 0:
                if gameinf.loc[prev[0] - 1, 'batter'] == gameinf.loc[prev, 'batter'].values[0] and gameinf.loc[prev, 'batter'].values[0] not in [gameinf.loc[index, 'batter'].values[0],gameinf.loc[index, 'first_baserunner'].values[0],
                                                                   gameinf.loc[index, 'second_baserunner'].values[0],
                                                                   gameinf.loc[index, 'third_baserunner'].values[0]]:
                    if 11 not in ast.literal_eval(data.loc[ind,'eventlist']) and 4 not in ast.literal_eval(data.loc[ind,'eventlist']) and otherouts == 0 and gameinf.loc[index, 'inning'].values != 10:
                        strikeouts += 1
                        #print(play,gameinf.loc[prev, 'batter'].values[0],gameinf.loc[index, 'batter'].values[0])
                        #print()
        data.loc[data.index[data['play_id'] == play - 1].tolist()[0],'strikeouts'] = strikeouts
        data.loc[data.index[data['play_id'] == play - 1].tolist()[0],'otherouts'] = otherouts
        #print(play,runners)



#print(data['otherouts'])
#print(sum(data['outathome']))
#print(sum(data['otherouts']) + sum(data['outathome']))

writer = 'MLBgamev5' + '.xlsx'
data.to_excel(writer)

















