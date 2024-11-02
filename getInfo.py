import pandas as pd
import numpy as np
from config import resultForPlayerColumn

#rowNum = 2836
#rowNum = 8106
#rowNum = 13510

dfNUmber = ['17926', '24333', '29031']
teams1 = ['Gliders2016', 'HELIOS2016']
teams2 = ['Oxsy', 'HfutEngine2017']
teams3 = ['Oxsy', 'HELIOS2016']
teamsCluster = [teams1, teams2, teams3]

for indexT, teams in enumerate(teamsCluster):
    lenResultDf = dfNUmber[indexT]
    #resFlagsTeam = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_list_withHidden_withZero_head.csv',)
    resFlagsTeam = pd.read_csv(f'./common_resultStaticsDf_process_more_{lenResultDf}_{teams[0]}-{teams[1]}_list_withZero_head.csv', sep=',')
    #resFlagsTeam = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_list_withHidden_withZero_head.csv',)
    #resFlagsTeam = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_list_withZero_head.csv',)
    print('test resFlagsTeam: ', resFlagsTeam)
    print(resFlagsTeam['strategyOpponent'])
    #print('test nuniq: ', resFlagsTeam['strategyOpponent'].nunique())
    def calcStats(calcDf):
        uniqueStrategy = calcDf['strategyOpponent'].unique()
        #print(' test read len', len(uniqueStrategy), uniqueStrategy)
        dicStatsUnique = {}
        for item in uniqueStrategy:
            print('strategy', item, len(calcDf[calcDf['strategyOpponent'] == item]))
        dicStatsUnique[item] = len(calcDf[calcDf['strategyOpponent'] == item])
        return dicStatsUnique

    #stats = calcStats(resFlagsTeam)

    newStatsDf = pd.DataFrame()
    newStatsDfTest = pd.DataFrame()
    limitRow = 4000
    limitRowTest = 200

    #allowStrategy = ['FrontalAttackGate', 'CenterSideSave', 'UpSideAttack', 'DownCenterSideSave', 'UpCenterSideSave']
    newStatsDf = resFlagsTeam.drop('strategyOpponent', axis=1)
    newStatsDf["strategyOpponent"] = ""
    #newStatsDf = newStatsDf.assign(e=pd.Series(np.random.randn(sLength)).values)
    #resFlagsTeam = resFlagsTeam.drop(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].index)
    # newStatsDf = newStatsDf.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].head(limitRow))
    # newStatsDfTest = pd.DataFramenewStatsDfTest.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].tail(limitRowTest))
    # newStatsDf = pd.concat([newStatsDf, newDf])
    # newStatsDfTest = pd.concat([sceletonStartDF, newDf])
    # для всех использовать переменную stats
    # for statistic in stats:
    #     #print(statistic)
    #     # if (stats[statistic] < limitRow):
    #     #     print('drop stats: ', statistic, stats[statistic])
    #     resFlagsTeam = resFlagsTeam.drop(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].index)
    #     if (stats[statistic] >= limitRow):
    #         print('not drop stats: ', statistic, stats[statistic])
    #         newStatsDf = newStatsDf.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].head(limitRow))
    #         #print('test len(newStatsDf) - limitRow):', len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]), len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]) - limitRow)
    #         numTail = len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]) - limitRow
    #         if numTail > 0:
    #             newStatsDfTest = newStatsDfTest.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].tail(limitRowTest))
    #             #newStatsDfTest = newStatsDfTest.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].tail(numTail))

    print("before export: ", len(resFlagsTeam))

    print("before newStatsDf: ", len(newStatsDf))

    print("before newStatsDfTest: ", len(newStatsDfTest))

    #calcStats(newStatsDf)

    # newStatsDf.to_csv(
    #     f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_list_withZero_head_cropped_withHidden.csv',
    #     index=False)
    #
    # newStatsDf.to_csv(
    #     f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_list_withZero_cropped_withHidden.csv',
    #     index=False, header=False)

    newStatsDf.to_csv(
        f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_{teams[0]}-{teams[1]}_list_withZero_head_cropped.csv',
        index=False)

    newStatsDf.to_csv(
        f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_{teams[0]}-{teams[1]}_list_withZero_cropped.csv',
        index=False, header=False)

    # ----------------

    # newStatsDfTest.to_csv(
    #     f'./common_resultStaticsDf_process_more_{len(newStatsDfTest)}_list_withZero_head_relustTest_{len(newStatsDf)}.csv',
    #     index=False)
    #
    # newStatsDfTest.to_csv(
    #     f'./common_resultStaticsDf_process_more_{len(newStatsDfTest)}_list_relustTest_{len(newStatsDf)}.csv',
    #     index=False, header=False)
