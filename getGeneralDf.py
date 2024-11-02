import pandas as pd
import numpy as np
from config import resultForPlayerColumn

dfNUmber = ['24623', '33971', '40798']
teams1 = ['Gliders2016', 'HELIOS2016']
teams2 = ['Oxsy', 'HfutEngine2017']
teams3 = ['Oxsy', 'HELIOS2016']
teamsCluster = [teams1, teams2, teams3]
numPeople = 11
gridLen = 6
gridWidth = 4

for indexT, teams in enumerate(teamsCluster):
    def readFile():
        resFlagsTeam = pd.DataFrame()
        item = dfNUmber[indexT]
        iter = pd.read_csv(f'./common_resultStaticsDf_process_more_{item}_{teams[0]}-{teams[1]}_withHead.csv', ',')
        resFlagsTeam = resFlagsTeam.append(iter, ignore_index=True)
        return resFlagsTeam

    resFlagsTeam = readFile()

    print(resFlagsTeam)

    resFlagsTeam.to_csv(
        f'./general_df_process_more_{len(resFlagsTeam)}_{teams[0]}-{teams[1]}_withHead.csv',
        index=False
    )

    # resFlagsTeam.to_csv(
    #     f'./general_df_process_more_{len(resFlagsTeam)}_withoutHead.csv',
    #     index=False, header=False)
