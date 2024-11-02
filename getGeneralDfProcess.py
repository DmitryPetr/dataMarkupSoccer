import pandas as pd
import numpy as np

dfNUmber = ['24623', '33971', '40798']
teams1 = ['Gliders2016', 'HELIOS2016']
teams2 = ['Oxsy', 'HfutEngine2017']
teams3 = ['Oxsy', 'HELIOS2016']
teamsCluster = [teams1, teams2, teams3]

#lenResultDf = 3060
numPeople = 11
gridLen = 6
gridWidth = 4

for indexT, teams in enumerate(teamsCluster):
    lenResultDf = dfNUmber[indexT]
    #generalDf = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead.csv', ',')
    #generalDf = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead_withHidden.csv', ',')
    #generalDf = pd.read_csv(f'./dataGeneral/general_df_process_more_{lenResultDf}_withHead.csv', ',')
    #generalDf = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead_withMerged.csv', ',')
    generalDf = pd.read_csv(f'./general_df_process_more_{lenResultDf}_{teams[0]}-{teams[1]}_withHead.csv', sep=',')


    print('Start df: ', len(generalDf))

    #     if (stats[statistic] < 120):
    #         print('drop stats: ', statistic, stats[statistic])
    #        # print('drop stats test: ', resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic])
    #         resFlagsTeam = resFlagsTeam.drop(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].index)

    print('test check one: ', len(generalDf[np.isnan(generalDf['yBall']) | np.isnan(generalDf['xBall'])]))

    generalDf = generalDf.drop(generalDf[np.isnan(generalDf['yBall']) | np.isnan(generalDf['xBall'])].index)
    #generalDf = generalDf.drop(generalDf[(generalDf[np.isnan(generalDf['xBall'])])].index)

    print('after drop nan ball coords: ', len(generalDf))

    generalDf = generalDf.drop(
        generalDf[
            (generalDf.yBall > 32.0) |
            (generalDf.yBall < -32.0) |
            (generalDf.xBall > 54.0) |
            (generalDf.xBall < -54.0)
            ].index
    )
    #generalDf = generalDf.drop(generalDf[(generalDf[np.isnan(generalDf['xBall'])])].index)

    print('after drop overflow ball coords: ', len(generalDf))


    generalDf.to_csv(
        f'./general_df_process_more_{len(generalDf)}_{teams[0]}-{teams[1]}_withHead_ball_check.csv',
        index=False
    )

    generalDf.to_csv(
        f'./general_df_process_more_{len(generalDf)}_{teams[0]}-{teams[1]}_withoutHead_ball_check.csv',
        index=False, header=False
    )

    # generalDf.to_csv(
    #     f'./general_df_process_more_{len(generalDf)}_withHead_withHidden.csv',
    #     index=False
    # )
    #
    # generalDf.to_csv(
    #     f'./general_df_process_more_{len(generalDf)}_withoutHead_withHidden.csv',
    #     index=False, header=False
    # )
