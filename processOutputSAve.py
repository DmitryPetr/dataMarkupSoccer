import pandas as pd
import numpy as np
from config import resultForPlayerColumn

teams = ['Gliders2016']
teams = ['Oxsy', 'HfutEngine2017']
numPeople = 11
#resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)

def readFile():
    resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
    for item in teams:
        for index in range(numPeople):
          # print(index, './data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv')
          iter = pd.read_csv('./data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv', ',')
          resFlagsTeam = resFlagsTeam.append(iter, ignore_index=True)
    return resFlagsTeam

resFlagsTeam = readFile()
# print(' test read', resFlagsTeam)
# print(' test read len', len(resFlagsTeam))

#uniqueStrategy = resFlagsTeam['strategyOpponent'].unique()
# print(' test read len', len(uniqueStrategy), uniqueStrategy)
#for item in uniqueStrategy:
#    print('strategy', item, len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == item]))
#print(' test read len', len(resFlagsTeam['strategyOpponent'].unique()))

# resFlagsTeam.to_csv(
#     './common_resultStaticsDf.csv',
#     index=False, header=None,)
endedDf = pd.DataFrame()
#for indexRow in range(len(resFlagsTeam)):

def getNameColumnIndex(resFlagsTeam: pd.DataFrame, nameColumn: str, indexRow: int, prefix: str):
    testStr = resFlagsTeam.at[indexRow, nameColumn]
    newArrayOpponent = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(np.float)
    newColomn = []
    for index in range(len(newArrayOpponent)):
        newColomn.append(f'{prefix}{index}')
    return newColomn


for indexRow in range(2):
    print('test concat indexRow: ', indexRow)
    newArrayOpponentOpponent = getNameColumnIndex(resFlagsTeam, 'opponentVector', indexRow, 'Op')
    print('get newArrayOpponentOpponent: ', newArrayOpponentOpponent)
    #testStr = resFlagsTeam.at[indexRow, 'opponentVector']
    #newArrayOpponentOpponent = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(np.float)
    # newColomn = []
    # for index in range(len(newArrayOpponent)):
    #     newColomn.append(f'Op{index}')
    # newDf = pd.DataFrame(data=newArrayOpponent, index=newColomn)
    testOneMore = pd.Series(resFlagsTeam.iloc[indexRow:indexRow+1, [0,1,2,3,4,5]].squeeze())
    print('test concat check testOneMore: ', testOneMore.reset_index(drop=True))
    print('test concat check newDf: ', newDf.transpose())
    testOneMore = pd.concat([testOneMore, newDf.transpose()], axis=1)
    print('test concat one: ', testOneMore)
    testStr = resFlagsTeam.at[indexRow, 'teamVector']
    newArrayOpponent = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(np.float)
    newColomn = []
    for index in range(len(newArrayOpponent)):
        newColomn.append(f'Tm{index}')
    newDf = pd.DataFrame(data=newArrayOpponent, index=newColomn)
    testOneMore = pd.concat([testOneMore, newDf.transpose()], axis=1, ignore_index=True)

    resFlagsTeam.loc[resFlagsTeam['sideTeam'] == 'left', ('sideTeam')] = 0
    endColumn = resFlagsTeam.iloc[indexRow:indexRow+1, [8, 9]]
    testOneMore = pd.concat([testOneMore, endColumn], axis=1)
    print('test concat three: ', testOneMore)
    endedDf.append(testOneMore)
print('test endedDf: ', endedDf)
#resFlagsTeam = readFile()