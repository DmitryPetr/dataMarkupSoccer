# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import numpy as np

# Create a dash application
from config import teams, strategyList, sizeTeam

app = dash.Dash(__name__)

global indexTeam
indexTeam = 0
global indexPlayer
indexPlayer = 0
global currentDf
currentDf = None

# REVIEW1: Clear the layout and do not display exception till callback gets executed
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
                html.Button('Сохранить', id='submit-val', n_clicks=0, style={'width': '30%', "height": '100%', 'margin-top': '10px'})
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
    def __init__(self, pathToImg, numRow):
        self.pathToImg = pathToImg
        self.numRow = numRow

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

    currentDf = pd.read_csv('./data/' + nowTeam + '_' + str(indexPlayer) + '_' + 'resultStaticsDf.csv', ',')
    currentDf['strategyOpponent'] = currentDf['strategyOpponent'].replace(np.nan, '**')

    print(currentDf)

def getPathFromNewImg():
    pathToImg: str = ''
    numRow: int = 0
    if not(currentDf.empty):
        for index, row in currentDf.iterrows():
            if row['strategyOpponent'] == '**':
                # indexTime = index
                print('tiem :: ', str(row['time']))
                pathToImg = str(row['time']) + '_' + teams[indexTeam] + '_' + str(indexPlayer) + '_' + 'resultStaticsImg.png'
                numRow = index
                break
    print('test pathToImg: ', pathToImg)
    return getPathImgResultI(pathToImg, numRow)

@app.callback(
               [
                   Output(component_id="testImg1", component_property='src'),
                   Output(component_id="paragraphOfSize", component_property='children'),
                   Output(component_id='inputTypeStrategy', component_property='value'),
                   Output(component_id='submit-val', component_property='n_clicks')
               ],
               [
                 Input(component_id='submit-val', component_property='n_clicks'),
                 Input(component_id='inputTypeStrategy', component_property='value')
               ]
             )
def processLoop(indexClick, selectStrategy):
    global indexPlayer
    global indexTeam
    global currentDf
    initPath = getPathFromNewImg()
    pathToImg = initPath.pathToImg
    indexNum: int = initPath.numRow
    print('indexTime', indexClick, selectStrategy, indexNum)
    if not(currentDf.empty) and indexClick > 0 and selectStrategy != None:
        print('in if processLoop', currentDf.at[indexNum, 'strategyOpponent'])
        currentDf.at[indexNum, 'strategyOpponent'] = selectStrategy
        if indexNum == 2: # len(currentDf)
            print('__ in if overflow len ++')
            indexPlayer += 1
            print('__ in if overflow indexPlayer add indexPlayer: ', indexPlayer)
            currentDf.to_csv('./data/output/' + teams[indexTeam] + '_' + str(indexPlayer) + '_' + 'resultStaticsDf_ok_process.csv', index=False)
            print('__ in if overflow bafore reread: ', indexPlayer)
            readLoopCsv()
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        # print('in if processLoop after',pathToImg, indexNum, currentDf.at[indexNum, 'strategyOpponent'])
        selectStrategy = None
    return [
        app.get_asset_url(pathToImg),
        f'Team: {teams[indexTeam]}, {str(indexNum + 1)} из {str(len(currentDf))}',
        selectStrategy,
        0
    ]

if __name__ == '__main__':
    readLoopCsv()
    print('main; ', currentDf)
    # indexTeam = initObj.indexTeam
    # indexPlayer = initObj.indexPlayer
    # currentDf = initObj.currentDf

    app.run_server()