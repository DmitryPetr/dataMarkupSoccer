import pandas as pd
import numpy as np
from config import strategyOnlyList, strategyMergeList

dfNUmber = ['472', '898', '1690']

lenResultDf = 3060
numPeople = 11
gridLen = 6
gridWidth = 4

def calcStats(calcDf):
    uniqueStrategy = calcDf['strategyOpponent'].unique()
    #print(' test read len', len(uniqueStrategy), uniqueStrategy)
    dicStatsUnique = {}
    for item in uniqueStrategy:
      print('strategy', item, len(calcDf[calcDf['strategyOpponent'] == item]))
      dicStatsUnique[item] = len(calcDf[calcDf['strategyOpponent'] == item])
    return dicStatsUnique

#generalDfHidden = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead.csv', ',')

#generalDf = pd.read_csv(f'./dataGeneral/general_df_process_more_{lenResultDf}_withHead.csv', ',')
#generalDfWithMerged = pd.read_csv(f'./withInfluence/general_df_process_more_{lenResultDf}_withHead.csv', ',')
generalDfWithMerged = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead_withHidden.csv', ',')
print(generalDfWithMerged)
print('Start before length: ', len(generalDfWithMerged))

stats = calcStats(generalDfWithMerged)

for strategy in strategyMergeList:
    for mergeItem in strategy['valueMerge']:
        #print('test testDf: ', mergeItem)
        query = generalDfWithMerged['strategyOpponent'] == mergeItem
        #print('test testDf query: ', query)
        generalDfWithMerged[query] = generalDfWithMerged[query].assign(strategyOpponent=strategy['value'])
        #print('test testDf query: ', generalDfWithMerged[query])
        #resultDf = resultDf.assign(strategyOpponent=strategy['value'])
        #resultDf['strategyOpponent'] = strategy['value']
        #print('test testDf: ', len(resutDf))
        #print('test testDf: ', resutDf['strategyOpponent'])
        #print('test testDf query fast before: ', generalDfWithMerged[query]['strategyOpponent'])
        #generalDfWithMerged[query]['strategyOpponent'] = strategy['value']
        #print('test testDf query fast: ', generalDfWithMerged[query]['strategyOpponent'])


print('Start after: ', generalDfWithMerged)

print('Start after length: ', len(generalDfWithMerged))

stats = calcStats(generalDfWithMerged)

generalDfWithMerged.to_csv(
    f'./general_df_process_more_{len(generalDfWithMerged)}_withHead_withMerged.csv',
    index=False)
