import pandas as pd
import numpy as np
from config import resultForPlayerColumn

# teams = ['Gliders2016', 'HELIOS2016']
teams = ['Oxsy', 'HfutEngine2017']

numPeople = 11
gridLen = 6
gridWidth = 4

# def readFile(pathToFileEnd):
#     resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
#     for item in teams:
#         for index in range(numPeople):
#           # if item == teams[1] and index > 3:
#           #     break
#           # print(index, './data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv')
#           #iter = pd.read_csv('./data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv', ',')
#           iter = pd.read_csv(f'./dataCSV/{item}_{str(index)}_{pathToFileEnd}.csv', ',')
#           #f'./dataCSV/{item}_{str(ind)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv'
#           resFlagsTeam = resFlagsTeam.append(iter, ignore_index=True)
#     return resFlagsTeam


# Old with manual preprocessed data
# for item in teams:
#     for index in range(numPeople):
#         # resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
#         #processedDf = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
#         processedDf = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
#         #processDf = pd.read_csv(f'./data/6x4/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
#         processDf = pd.read_csv(f'./data/6x4/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
#         print("___ test ")
#         processDf['strategyOpponent'] = processedDf['strategyOpponent']

#         processDf.to_csv(
#             f'./data/output6x4/{item}_{str(index)}__resultStaticsDf_ok_process.csv',
#             index=False)
        
for item in teams:
    for index in range(numPeople):
        # resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
        #processedDf = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
        processedDf = pd.read_csv(f'./data/data/dataForStrategy/{teams[0]}-{teams[1]}/{item}_{str(index)}_{str(gridLen)}_{str(gridWidth)}.csv', ',')
        #processDf = pd.read_csv(f'./data/6x4/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
        processDf = pd.read_csv(f'./data/6x4/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
        print("___ test ")
        processDf['strategyOpponent'] = processedDf['strategyOpponent']

        processDf.to_csv(
            f'./data/output6x4/{item}_{str(index)}__resultStaticsDf_ok_process.csv',
            index=False)