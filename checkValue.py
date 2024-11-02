import pandas as pd
import numpy as np
from config import resultForPlayerColumn

#rowNum = 13510
#rowNum = 8106
rowNum = 2836

#dfRead = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_withHead_withAddValue.csv', ',')
#dfRead = pd.read_csv(f'./general_df_process_more_{rowNum}_withHead.csv', ',')
dfRead = pd.read_csv(f'./general_df_process_more_{rowNum}_withHead.csv', ',')
#dfRead = pd.read_csv(f'./dataGeneral/general_df_process_more_{rowNum}_withHead.csv', ',')
# dfRead = pd.read_csv(
#     f'./general_df_process_more_{rowNum}_withHead.csv', ',')
#    f'./common_resultStaticsDf_process_more_{rowNum}_withHead_withAddValue.csv', ',')

print(dfRead)
#print(dfRead.drop(['x', 'y', 'angle', 'xBall', 'yBall'], axis=1))
dfRead = dfRead.drop(['x', 'y', 'angle', 'xBall', 'yBall'], axis=1)
#dfRead = dfRead.drop(['x', 'y', 'angle', 'xBall', 'yBall', 'sumOp', 'sumTm', 'sumAll'], axis=1)
print('after drop', dfRead)
dfRead.loc[dfRead['sideTeam'] == 'rigth', ('sideTeam')] = 1
#dfRead = dfRead.loc[:, dfRead.any()]
print(dfRead)
# dfRead.to_csv(
#     f'./common_resultStaticsDf_process_more_{rowNum}_list_check.csv',
#     index=False)
#dfRead = pd.read_csv('./common_resultStaticsDf_process_more_482_v2_withHead.csv', ',')

dfRead.to_csv(
    f'./common_resultStaticsDf_process_more_{rowNum}_list_withZero_head.csv',
    index=False)

dfRead.to_csv(
    f'./common_resultStaticsDf_process_more_{rowNum}_list_withZero.csv',
    index=False, header=False)


# dfRead.to_csv(
#     f'./common_resultStaticsDf_process_more_{rowNum}_list_withHidden_withZero_head.csv',
#     index=False)
#
# dfRead.to_csv(
#     f'./common_resultStaticsDf_process_more_{rowNum}_list_withHidden_withZero.csv',
#     index=False, header=False)