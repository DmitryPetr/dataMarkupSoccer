import pandas as pd
import numpy as np
import random

rowNum = 2836

iterNumber = 4

#dfRead = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_withHead.csv', ',')
dfRead = pd.read_csv(f'./general_df_process_more_{rowNum}_withHead.csv', ',')
#dfRead = pd.read_csv(f'./dataGeneral/general_df_process_more_{rowNum}_withHead.csv', ',')
print(dfRead)

def calcNumberAgentTick(row, name):
    size = 23
    sumAgent = 0
    for item in range(size):
        sumAgent += row[f'{name}{item}']
    return sumAgent

dfRead['sumOp'] = 0
dfRead['sumTm'] = 0
dfRead['sumAll'] = 0

def calcSumValueAgentDf(dfRead):
    for index, row in dfRead.iterrows():
        row['sumOp'] = calcNumberAgentTick(row, 'Op')
        row['sumTm'] = calcNumberAgentTick(row, 'Tm')
        row['sumAll'] = row['sumOp'] + row['sumTm']
        dfRead.at[index, 'sumOp'] = row['sumOp']
        dfRead.at[index, 'sumTm'] = row['sumTm']
        dfRead.at[index, 'sumAll'] = row['sumAll']
        #print(dfRead[index])
        # if row['sumAll'] < 11:
        #     print(index, row['sumOp'], row['sumTm'], row['sumAll'])
    return dfRead

def getStatisticSumAgentDf(dfRead):
    print('sumOp max: ', dfRead['sumOp'].max())
    print('sumOp min: ', dfRead['sumOp'].min())
    print('sumTm max: ', dfRead['sumTm'].max())
    print('sumTm min: ', dfRead['sumTm'].min())
    print('sumAll max: ', dfRead['sumAll'].max())
    print('sumAll min: ', dfRead['sumAll'].min())
    print('__ dfRead Len: ', len(dfRead))

dfRead = calcSumValueAgentDf(dfRead)

dfRead = dfRead.drop(dfRead[dfRead['sumAll'] < 11].index)

getStatisticSumAgentDf(dfRead)

def generateNewRowForAgentTick(row, name, indexRow, roundADd):
    size = 23
    newRow = row.copy(deep=True)
    for item in range(size):
        curVal = row[f'{name}{item}']
        if curVal == 0:
            continue
        #print('\nStart value: ',indexRow, item, name, curVal, roundADd)
        additionalVal = random.randrange(-2, 3, 1)
        if additionalVal < 0 and np.abs(additionalVal) > curVal:
            curVal = np.abs(additionalVal) - curVal
        else:
            curVal += additionalVal
        #print('Value process: ',curVal, additionalVal)
        if curVal < 0:
            curVal = 0
        if curVal != newRow[f'{name}{item}']:
            #print('\n_____ ROW add: ')
           # print('indexRow: ',indexRow)
            #print('item index name: ',item, name)
            #print('Not Equal value: ',curVal, row[f'{name}{item}'])
            #print('_____ ROW add end: ')
            newRow[f'{name}{item}'] = curVal
    return newRow

newDf = dfRead.copy(deep=True)

for index, row in dfRead.iterrows():
    # if index > 1:
    #     break
    for roundADd in range(iterNumber):
        print('calc roundADd: ', index, roundADd)
        #print(row)
        newRowOp = generateNewRowForAgentTick(row, 'Op', index, roundADd)
        newRowTm = generateNewRowForAgentTick(newRowOp, 'Tm', index, roundADd)
        #print(newRowTm)
        newDf = newDf.append(newRowTm)
    # row['sumOp'] = calcNumberAgentTick(row, 'Op')
    # row['sumTm'] = calcNumberAgentTick(row, 'Tm')
    # row['sumAll'] = row['sumOp'] + row['sumTm']
    # dfRead.at[index, 'sumOp'] = row['sumOp']
    # dfRead.at[index, 'sumTm'] = row['sumTm']
    # dfRead.at[index, 'sumAll'] = row['sumAll']

getStatisticSumAgentDf(newDf)

newDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(newDf)}_withHead_withAddValue.csv',
    index=False)