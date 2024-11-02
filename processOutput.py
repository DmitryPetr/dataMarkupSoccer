import pandas as pd
import numpy as np
from config import resultForPlayerColumn

#teams = ['Gliders2016', 'HELIOS2016']
#teams = ['Oxsy', 'HfutEngine2017']
teams = ['Oxsy', 'HELIOS2016']
numPeople = 11
gridLen = 6
gridWidth = 4
#resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)

# Next: getGeneralDf -> getGeneralDfProcess -> checkValue ->getInfo

def readFile():
    resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
    for item in teams:
        for index in range(numPeople):
          # if item == teams[1] and index > 3:
          #     break
          # print(index, './data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv')
          # iter = pd.read_csv(f'./data/output/{item}_{str(index)}__resultStaticsDf_ok_process.csv', ',')
          # iter = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
          #iter = pd.read_csv(f'./data/output6x4/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
          # iter = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', ',')
          #print('test file: ', f'{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}_withHidden.csv')
          #iter = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}_withHidden.csv', ',')
          iter = pd.read_csv(f'./data/dataForStrategy/{teams[0]}-{teams[1]}/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv', sep=',')
          #print('test readDf before drop infos: ', item, index)
          #print('test readDf before drop duplicates: ', len(iter))
          iter = iter.drop_duplicates(subset='time', keep="first")
          #print('test readDf after drop duplicates: ', len(iter))
          resFlagsTeam = resFlagsTeam.append(iter, ignore_index=True)
    return resFlagsTeam

resFlagsTeam = readFile()
print('test resFlagsTeam: ')
print(resFlagsTeam['strategyOpponent'])
#print('test nuniq: ', resFlagsTeam['strategyOpponent'].nunique())
def calcStats():
    uniqueStrategy = resFlagsTeam['strategyOpponent'].unique()
    #print(' test read len', len(uniqueStrategy), uniqueStrategy)
    dicStatsUnique = {}
    for item in uniqueStrategy:
      print('strategy', item, len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == item]))
      dicStatsUnique[item] = len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == item])
    return dicStatsUnique

stats = calcStats()
print(stats)
# for statistic in stats:
#     #print(statistic)
#     if (stats[statistic] < 120):
#         print('drop stats: ', statistic, stats[statistic])
#        # print('drop stats test: ', resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic])
#         resFlagsTeam = resFlagsTeam.drop(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].index)
resFlagsTeam = resFlagsTeam.reset_index(drop=True)
# print('test resFlagsTeam: ', resFlagsTeam)
stats = calcStats()

# resFlagsTeam.to_csv(
#     './common_resultStaticsDf.csv',
#     index=False)

class getNameColumnIndexI:
    def __init__(self, newNaneColomn, newArrayFromStr):
        self.newNaneColomn = newNaneColomn
        self.newArrayFromStr = newArrayFromStr

def getNameColumnIndex(resFlagsTeam: pd.DataFrame, nameColumn: str, indexRow: int, prefix: str):
    #print('getNameColumnIndex get: ', type(indexRow), type(nameColumn))
    #print('getNameColumnIndex get indexRow: ', resFlagsTeam[indexRow])
    testStr = resFlagsTeam.at[indexRow, nameColumn]
    #print('test getNameColumnIndex testStr: ', testStr)
    #newArrayFromStr = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(float)
    newArrayFromStr = np.array(testStr.replace('[', '').replace(']', '').split(', '))
    newNaneColomn = []
    for index in range(len(newArrayFromStr)):
        newNaneColomn.append(f'{prefix}{index}')
    return getNameColumnIndexI(newNaneColomn, newArrayFromStr)


forColumnArray = ['x', 'y', 'angle', 'xBall','yBall']
#forColumnArray = ['time', 'x', 'y', 'angle', 'xBall','yBall']
# Колонки  двумя колонками векторов для противников и союзников
# forColumnOpponentObj = getNameColumnIndex(resFlagsTeam, 'opponentVector', 0, 'Op')
# forColumnArray = forColumnArray + forColumnOpponentObj.newNaneColomn
# forColumnTeamObj = getNameColumnIndex(resFlagsTeam, 'teamVector', 0, 'Tm')
# forColumnArray = forColumnArray + forColumnTeamObj.newNaneColomn

#forColumnOpponentInluenceObj = getNameColumnIndex(resFlagsTeam, 'opponentInfluenceVector', 0, 'OpInfl')
forColumnArray = forColumnArray #+ forColumnOpponentInluenceObj.newNaneColomn

forColumnArray = forColumnArray + ['sideTeam', 'strategyOpponent']
#print('end forColumnArray: ', forColumnArray)
endedDf = pd.DataFrame(columns=forColumnArray)

# print('test endedDf: ', endedDf)

for indexRow in range(len(resFlagsTeam)):
    print('test concat indexRow: ', indexRow)
    sceletonStartDF = pd.Series(resFlagsTeam.iloc[indexRow:indexRow+1, [1,2,3,4,5]].squeeze())
    #print('test sceletonStartDF: ', sceletonStartDF)

    #newOpponentInfluenceObj = getNameColumnIndex(resFlagsTeam, 'opponentInfluenceVector', indexRow, 'OpInfl')
    #newDf = pd.Series(newOpponentInfluenceObj.newArrayFromStr, index=newOpponentInfluenceObj.newNaneColomn)
    sceletonStartDF = pd.concat([sceletonStartDF])

    # Вариант с двумя векторами
    newOpponentObj = getNameColumnIndex(resFlagsTeam, 'opponentVector', indexRow, 'Op')
    newDf = pd.Series(newOpponentObj.newArrayFromStr, index=newOpponentObj.newNaneColomn)
    sceletonStartDF = pd.concat([sceletonStartDF, newDf])
    
    newTeamObj = getNameColumnIndex(resFlagsTeam, 'teamVector', indexRow, 'Tm')
    newDf = pd.Series(newTeamObj.newArrayFromStr, index=newTeamObj.newNaneColomn)
    sceletonStartDF = pd.concat([sceletonStartDF, newDf])

    #print('after end serias: ', sceletonStartDF)

    resFlagsTeam.loc[resFlagsTeam['sideTeam'] == 'left', ('sideTeam')] = 0
    resFlagsTeam.loc[resFlagsTeam['sideTeam'] == 'rigth', ('sideTeam')] = 1
    endColumn = pd.Series(resFlagsTeam.iloc[indexRow:indexRow+1, [8, 9]].squeeze())
    sceletonStartDF = pd.concat([sceletonStartDF, endColumn])
    sceletonStartDF.name = indexRow
    #print('test concat three: ', sceletonStartDF)
    endedDf = endedDf.append(sceletonStartDF, ignore_index=False)
# print('test endedDf: ', endedDf)

endedDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(resFlagsTeam)}_{teams[0]}-{teams[1]}_withHead.csv',
    index=False)

endedDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(resFlagsTeam)}_{teams[0]}-{teams[1]}_withoutHead.csv',
    index=False, header=False)



#, header=False