import pandas as pd
import numpy as np

dfNUmber = ['472', '898', '1690']

lenResultDf = 3060
numPeople = 11
gridLen = 6
gridWidth = 4

generalDfHidden = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead.csv', ',')

generalDf = pd.read_csv(f'./dataGeneral/general_df_process_more_{lenResultDf}_withHead.csv', ',')

#print('Start df: ', len(generalDf))

# print('watch: ', generalDf)
# print('watch one: ', generalDfHidden)

# print('watch strategyOpponent: ', generalDf['strategyOpponent'])
# print('watch one strategyOpponent: ', generalDfHidden['strategyOpponent'])

generalDfHidden['strategyOpponent'] = generalDf['strategyOpponent']

# print('watch after strategyOpponent: ', generalDf['strategyOpponent'])
# print('watch one after strategyOpponent: ', generalDfHidden['strategyOpponent'])

print('watch after: ', generalDf)
print('watch one after: ', generalDfHidden)

generalDfHidden.to_csv(
    f'./general_df_process_more_{len(generalDf)}_withHead_withInfluence.csv',
    index=False)
