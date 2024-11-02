# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
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
        return
        # indexTeam = 0

    nowTeam = teams[indexTeam]

    currentDf = pd.read_csv(f'./data/{nowTeam}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
    currentDf['strategyOpponent'] = currentDf['strategyOpponent'].replace(np.nan, '**')

    print(currentDf)

def getPathFromNewImg():
    pathToImg: str = ''
    numRow: int = -1
    sideStr: str = ''
    if not(currentDf.empty):
        for index, row in currentDf.iterrows():
            if row['strategyOpponent'] == '**':
                # indexTime = index
                pathToImg = str(row['time']) + '_' + teams[indexTeam] + '_' + str(indexPlayer) + '_' + 'resultStaticsImg.png'
                numRow = index
                sideStr = row['sideTeam'] + ', Ball: ' + str(row['xBall']) + ' ' + str(row['yBall'])
                break
    return getPathImgResultI(pathToImg, numRow, sideStr)

def saveCurrentProggres(indexNum):
    global indexPlayer
    global indexTeam
    global currentDf
    currentTime = currentDf.at[0 if indexNum == -1 else indexNum, 'time']
    #currentTime = currentDf.at[indexNum, 'time']
    entropyName = randint(1000, 100000)
    currentDf.to_csv(
        f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_{currentTime}_resultStaticsDf_curpr_{str(entropyName)}.csv',
        index=False)




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
    # saveClicks = 0
    global indexPlayer
    global indexTeam
    global currentDf
    initPath = getPathFromNewImg()
    pathToImg = initPath.pathToImg
    indexNum: int = initPath.numRow
    sideStr: str = initPath.sideStr
    if saveClicks > 0:
        saveCurrentProggres(indexNum)
    if not(currentDf.empty) and indexClick > 0 and saveClicks == 0 and selectStrategy != None:
        currentDf.at[indexNum, 'strategyOpponent'] = selectStrategy
        if indexNum == len(currentDf) - 1:
            currentDf.to_csv(
                f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv',
                index=False)
            indexPlayer += 1
            readLoopCsv()
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        sideStr = initPath.sideStr
        # print('in if processLoop after',pathToImg, indexNum, currentDf.at[indexNum, 'strategyOpponent'])
        selectStrategy = None
    if indexNum ==  -1:
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