# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import numpy as np
from random import randint

# Create a dash application
from config import teams, strategyList, sizeTeam, gridLen, gridWidth

app = dash.Dash(__name__)

global indexTeam
indexTeam = 0
global indexPlayer
indexPlayer = 0
global currentDf
currentDf = None



# REVIEW1: Clear the layout and do not display exforception till callback gets executed
app.config.suppress_callback_exceptions = True


# Application layout
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id='inputTypeStrategy',
                         options=strategyList,
                         placeholder="Стратегии",
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
                html.Div([
                    html.Button('Разметить', id='submit-val', n_clicks=0, style={'width': '30%', "height": '100%', 'margin-top': '10px'}),
                    html.Button('Сохранить прогресс', id='save-val', n_clicks=0, style={'width': '30%', "height": '100%', 'margin-top': '10px', 'margin-left': '10px'}),
                ])
            ]),
        ]),
        html.Div(id='paragraphOfSize', style={'margin-top': '10px', 'margin-left': '10px', 'font-size': '18px'}),
        html.Img(id='testImg1', style={'width': '100%', "height": '50%', 'border': 'solid 1px black'}),
    ]),

])


class readImageLoopResultI:
    def __init__(self, indexTime, pathToImg):
        self.indexTime = indexTime
        self.pathToImg = pathToImg

# class readCsvLoopResultI:
#     def __init__(self, indexTeam, indexPlayer, currentDf):
#         self.indexTeam = indexTeam
#         self.indexPlayer = indexPlayer
#         self.currentDf = currentDf

class getPathImgResultI:
    def __init__(self, pathToImg, numRow, sideStr):
        self.pathToImg = pathToImg
        self.numRow = numRow
        self.sideStr = sideStr

def readLoopCsv():
    global indexPlayer
    global indexTeam
    global currentDf

    if indexPlayer >= sizeTeam:
        indexTeam += 1
        indexPlayer = 0

    if indexTeam >= len(teams):
        print('__ in readLoopCsv return: ', indexTeam)
        return
        # indexTeam = 0

    nowTeam = teams[indexTeam]

    print('__ in readLoopCsv : ', nowTeam, indexPlayer)

    currentDf = pd.read_csv(f'./data/{nowTeam}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
    currentDf['strategyOpponent'] = currentDf['strategyOpponent'].replace(np.nan, '**')

    print(currentDf)

def getPathFromNewImg():
    print('getPathFromNewImg start')
    pathToImg: str = ''
    numRow: int = -1
    sideStr: str = ''
    if not(currentDf.empty):
        print('getPathFromNewImg not empty')
        for index, row in currentDf.iterrows():
            if row['strategyOpponent'] == '**':
                # indexTime = index
                print('tiem :: ', str(row['time']))
                pathToImg = str(row['time']) + '_' + teams[indexTeam] + '_' + str(indexPlayer) + '_' + 'resultStaticsImg.png'
                numRow = index
                print('getPathFromNewImg before sideTeam: ', row['sideTeam'] )
                sideStr = row['sideTeam'] + ', Ball: ' + str(row['xBall']) + ' ' + str(row['yBall'])
                break
    print('test pathToImg: ', pathToImg, numRow)
    return getPathImgResultI(pathToImg, numRow, sideStr)

def saveCurrentProggres(indexNum):
    print('saveCurrentProggres')
    global indexPlayer
    global indexTeam
    global currentDf
    currentTime = currentDf.at[0 if indexNum == -1 else indexNum, 'time']
    #currentTime = currentDf.at[indexNum, 'time']
    entropyName = randint(1000, 100000)
    print('saveCurrentProggres end', currentTime, str(entropyName))
    currentDf.to_csv(
        f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_{currentTime}_resultStaticsDf_curpr_{str(entropyName)}.csv',
        index=False)
    print('saveCurrentProggres end')




@app.callback(
               [
                   Output(component_id="testImg1", component_property='src'),
                   Output(component_id="paragraphOfSize", component_property='children'),
                   Output(component_id='inputTypeStrategy', component_property='value'),
                   Output(component_id='submit-val', component_property='n_clicks'),
                   Output(component_id='save-val', component_property='n_clicks')
               ],
               [
                 Input(component_id='submit-val', component_property='n_clicks'),
                 Input(component_id='save-val', component_property='n_clicks'),
                 Input(component_id='inputTypeStrategy', component_property='value')
               ]
             )
def processLoop(indexClick, saveClicks, selectStrategy):
    print('processLoop start')
    # saveClicks = 0
    global indexPlayer
    global indexTeam
    global currentDf
    print('processLoop test before getPathFromNewImg')
    initPath = getPathFromNewImg()
    pathToImg = initPath.pathToImg
    indexNum: int = initPath.numRow
    sideStr: str = initPath.sideStr
    print('processLoop test after getPathFromNewImg')
    if saveClicks > 0:
        saveCurrentProggres(indexNum)
    print('indexTime', indexClick, selectStrategy, indexNum)
    if not(currentDf.empty) and indexClick > 0 and saveClicks == 0 and selectStrategy != None:
        print('in if processLoop', currentDf.at[indexNum, 'strategyOpponent'])
        currentDf.at[indexNum, 'strategyOpponent'] = selectStrategy
        print('__ in if overflow qual ++', indexNum, len(currentDf))
        if indexNum == len(currentDf) - 1:
            print('__ in if overflow len ++')
            currentDf.to_csv(
                f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv',
                index=False)
            indexPlayer += 1
            print('__ in if overflow indexPlayer add indexPlayer: ', indexPlayer)
            print('__ in if overflow bafore reread: ', indexPlayer)
            readLoopCsv()
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        sideStr = initPath.sideStr
        # print('in if processLoop after',pathToImg, indexNum, currentDf.at[indexNum, 'strategyOpponent'])
        selectStrategy = None
    if indexNum ==  -1:
        print('__ in if -1 len ++')
        exitIndex = indexNum
        while exitIndex == -1:
            indexPlayer += 1
            readLoopCsv()
            getObj = getPathFromNewImg()
            exitIndex = getObj.numRow
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        sideStr = initPath.sideStr
    return [
        app.get_asset_url(pathToImg),
        f'Team: {teams[indexTeam]}, {str(indexNum + 1)} из {str(len(currentDf) + 1)}, сторона - {sideStr}',
        selectStrategy,
        0,
        0
    ]

if __name__ == '__main__':
    num = 5 * 7
    print(num)

    # Тут главная программа
    # readLoopCsv()
    # print('main; ', currentDf)
    #
    # # indexTeam = initObj.indexTeam
    # # indexPlayer = initObj.indexPlayer
    # # currentDf = initObj.currentDf
    #
    # app.run_server()