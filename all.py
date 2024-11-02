predict - strategy - RoboCup /
for -predict - strategy.ipynb

import pandas as pd
import numpy as np
import matplotlib as mpl
import tabulate

from IPython.display import display
from sklearn.preprocessing import LabelEncoder
from sklearn import cluster
from tensorflow import keras
from IPython.core.formatters import format_display_data
from matplotlib import pyplot as plt
import seaborn as sns

mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['figure.facecolor'] = '1'

rowNum = 2836
rowNumTest = 400
df = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_list_withZero_head.csv')

dfTest = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNumTest}_list_relustTest_8000.csv')

max_review_op_length = df.shape[1] - 2
newIndex = np.arange(0, max_review_op_length)
max_review_length = df.shape[1] - 1
max_review_length_last = max_review_length - 1
newIndexDataArr = np.append(newIndex, max_review_length_last)

value_tactic = len(df['strategyOpponent'].unique())
dataset = df.values

X = dataset[:, newIndexDataArr].astype(float)
Y = dataset[:, max_review_length]

print('X test: ', X)
print('Y test: ', Y)

datasetTest = dfTest.values
XTest = datasetTest[:, newIndexDataArr].astype(float)
YTest = datasetTest[:, max_review_length]

encoder = LabelEncoder()
Y_e = encoder.fit_transform(Y)
Y_d = keras.utils.to_categorical(Y_e)

Y_e_test = encoder.fit_transform(YTest)
Y_d_test = keras.utils.to_categorical(Y_e_test)

from sklearn.preprocessing import StandardScaler

X = pd.DataFrame(StandardScaler().fit_transform(X)).to_numpy()

import seaborn as sns
import warnings
from matplotlib.colors import ListedColormap

PALETTE = sns.color_palette('deep', n_colors=10)
CMAP = ListedColormap(PALETTE.as_hex())


def plot_iris_2d(x, y, title, c_in=Y_e, xlabel="1st eigenvector", ylabel="2nd eigenvector"):
    sns.set_style("darkgrid")

    plt.scatter(x, y,
                c=c_in,
                cmap=CMAP,
                s=2)

    plt.title(title, fontsize=20, y=1.03)

    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)


def get_columns_with_pref(prefix, num_components):
    COLUMNS = []
    for i in range(num_components):
        COLUMNS.append(f'{prefix}{i}')
    return COLUMNS


from sklearn.decomposition import PCA

num_components = 2

pca = PCA(n_components=num_components)
points_pca = pca.fit_transform(X)

data_pca = pd.DataFrame(points_pca, columns=get_columns_with_pref('PC', num_components))
sns.heatmap(data_pca.corr())

plot_iris_2d(
    x=data_pca['PC0'],
    y=data_pca['PC1'],
    title='PCA')
plt.savefig('./img' + '_PCA_' + '_' + 'resultImg_.png', format='png', dpi=600)

from sklearn.decomposition import PCA

num_components = 2

pca = PCA(n_components=num_components)
points_pca = pca.fit_transform(X)

from sklearn.manifold import TSNE

RANDOM_STATE = 42
tsne_n_components = 2
history_tsne = []

with warnings.catch_warnings():
    # tsne = TSNE(n_components=tsne_n_components, perplexity=40, n_iter=2000, random_state=RANDOM_STATE, method='exact')
    # tsne = TSNE(n_components=tsne_n_components, n_iter=5000, random_state=RANDOM_STATE, method='exact')
    tsne = TSNE(n_components=tsne_n_components, perplexity=40, n_iter=2000, random_state=RANDOM_STATE,
                method='barnes_hut')
    points = tsne.fit_transform(X)
history_tsne.append(points)

pd_tsneArray = []
for item in history_tsne:
    pd_tsneArray.append(pd.DataFrame(item, columns=get_columns_with_pref('cl', tsne_n_components)))

data_tsne = pd.DataFrame(points, columns=get_columns_with_pref('cl', tsne_n_components))
sns.heatmap(data_tsne.corr())

## 2d

plot_num = 1
# axes[0, 0]
for item in pd_tsneArray:
    plt.subplots(1, 1)
    plot_iris_2d(
        x=item['cl0'],
        y=item['cl1'],
        title='TSNE_index_' + str(plot_num))
    plot_num += 1
    # plt.savefig('./img' + str(plot_num) + '_t-sne_' + '_' + 'resultImg_.png', format='png', dpi=600)

# 3d - using with tsne_n_components = 3

from mpl_toolkits.mplot3d import Axes3D


def plot_iris_3d(x, y, z, title, c_in=Y_e):
    sns.set_style('whitegrid')

    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)

    ax.scatter(x, y, z,
               c=c_in,
               cmap=CMAP,
               s=2)

    ax.set_title(title, fontsize=20, y=1.03)

    fsize = 14
    ax.set_xlabel("1st eigenvector", fontsize=fsize)
    ax.set_ylabel("2nd eigenvector", fontsize=fsize)
    ax.set_zlabel("3rd eigenvector", fontsize=fsize)

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])


## 3d

plot_num = 0
# axes[0, 0]
item = pd_tsneArray[plot_num]
plot_iris_3d(
    x=item['cl0'],
    y=item['cl1'],
    z=item['cl2'],
    title='TSNE')
plt.savefig('./img/' + str(plot_num) + '_t-sne_3d_' + '_' + 'resultImg_.png', format='png', dpi=600)

# Search knee in data for set DBScan prams

import numpy as np
from sklearn.neighbors import NearestNeighbors

# n_neighbors = 5 as kneighbors function returns distance of point to itself (i.e. first column will be zeros)
n_neighbors = 5
pointsNN = history_tsne[0]
nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(pointsNN)
# Find the k-neighbors of a point
neigh_dist, neigh_ind = nbrs.kneighbors(pointsNN)
# sort the neighbor distances (lengths to points) in ascending order
# axis = 0 represents sort along first axis i.e. sort along row
sort_neigh_dist = np.sort(neigh_dist, axis=0)

import matplotlib.pyplot as plt

k_dist = sort_neigh_dist[:, n_neighbors - 1]
plt.plot(k_dist)
plt.axhline(y=1.7, linewidth=1, linestyle='dashed', color='k')
plt.ylabel("k-NN distance")
plt.xlabel("Sorted observations (4th NN)")
plt.show()

pointsCalc = history_tsne[0]

# Get clustering

import warnings
from itertools import cycle, islice

# dbscan = cluster.DBSCAN(eps=3.3, min_samples=5)
dbscan = cluster.OPTICS(min_samples=5,
                        xi=0.03,
                        min_cluster_size=0.03, )

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        message="the number of connected components of the "
                + "connectivity matrix is [0-9]{1,2}"
                + " > 1. Completing it to avoid stopping the tree early.",
        category=UserWarning,
    )
    warnings.filterwarnings(
        "ignore",
        message="Graph is not fully connected, spectral embedding"
                + " may not work as expected.",
        category=UserWarning,
    )
    dbscan.fit(pointsCalc)

if hasattr(dbscan, "labels_"):
    y_pred = dbscan.labels_.astype(int)
else:
    y_pred = dbscan.predict(pointsCalc)

colors = np.array(
    list(
        islice(
            cycle(
                [
                    "#377eb8",
                    "#ff7f00",
                    "#4daf4a",
                    "#f781bf",
                    "#a65628",
                    "#984ea3",
                    "#999999",
                    "#e41a1c",
                    "#dede00",
                    "#377ef3",
                    "#ff7f11",
                    "#4daf43",
                    "#f78154",
                    "#a65676",
                    "#984e3a",
                    "#999944",
                    "#e41ac8",
                    "#dede39",
                    "#dede11",
                ]
            ),
            int(max(y_pred) + 1),
        )
    )
)

display(np.unique(dbscan.labels_))
plt.scatter(pointsCalc[:, 0], pointsCalc[:, 1], s=1, color=colors[y_pred])
# plt.xticks(())
# plt.yticks(())

# plt.show()

data_tsne['strategy'] = df['strategyOpponent']
display(data_tsne['strategy'].value_counts())

# df_process = pd.DataFrame(data_tsne)
df_process = pd.DataFrame(pd_tsneArray[0])
# df_process['strategy'] = df['strategyOpponent']#dbscan.labels_
df_process['strategy'] = dbscan.labels_
display(df_process['strategy'].value_counts())
df_process = df_process.drop(df_process[df_process['strategy'] == - 1].index)
display(df_process['strategy'].value_counts())

display(len(df_process.value_counts(df_process['strategy'])))
df_process.value_counts(df_process['strategy'])

# View clastering

sns.scatterplot(data=df_process, x="cl0", y="cl1", hue="strategy", s=4, palette='deep')
plt.savefig('./img/' + str(plot_num) + '_optics_' + '_' + 'resultImg_.png', format='png', dpi=600)

plot_iris_3d(
    x=df_process['cl0'],
    y=df_process['cl1'],
    z=df_process['cl2'],
    title='TSNE', c_in=df_process['strategy'])
plt.savefig('./img/' + str(plot_num) + '_dbscan_3d_' + '_' + 'resultImg_.png', format='png', dpi=600)

# Обучение без учителя

from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(df_process, df_process['strategy'], test_size=0.1, random_state=42)

# Обучение с учителем и с сжатием данных

from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(data_tsne, data_tsne['strategy'], test_size=0.1, random_state=42)

# Обучение без учителя

x_train = x_train.drop('strategy', axis=1)
x_val = x_val.drop('strategy', axis=1)

Y_e = encoder.fit_transform(y_train.values)
Y_d = keras.utils.to_categorical(Y_e)

Y_e_test = encoder.fit_transform(y_val.values)
Y_d_test = keras.utils.to_categorical(Y_e_test)

X = x_train.values
XTest = x_val.values

Y_d

print(Y_d_test.shape[1])

value_tactic = Y_d_test.shape[1]
model = keras.models.Sequential([
    keras.layers.Dense(15, activation='relu'),
    keras.layers.Dense(value_tactic, activation='sigmoid')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X, Y_d, epochs=5, batch_size=10, validation_split=0.1, verbose=1)
score = model.evaluate(XTest, Y_d_test)

# score
print("Точность обучения: {0:.2%}".format(score[1]))


def plot_history(history, ax1=None, ax2=None, nameSave=None):
    df_h = pd.DataFrame(history.history)
    if ax1 is None:
        _, [ax1, ax2] = plt.subplots(1, 2, figsize=(12, 6))
    df_h[['accuracy', 'val_accuracy']].plot(ax=ax1, fontsize=18)
    df_h[['loss', 'val_loss']].plot(ax=ax2, fontsize=18)
    for ax in [ax1, ax2]:
        ax.legend(fontsize=18)
        ax.set_xlabel('epoch', fontsize=18)
        # ax.rc(fontsize=20)
        ax.grid(0.75)
        ax.set_axisbelow(True)

    if nameSave:
        plt.savefig(nameSave, format='png', dpi=600)


plot_history(history)
plt.gcf().tight_layout()
# plt.savefig('h0.png')

from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)

histories = []
scores = []
neyron = 15  # max_review_op_length+1
# neyron = max_review_op_length+1

for train_index, test_index in kf.split(X, Y_d):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y_d[train_index], Y_d[test_index]
    model = keras.models.Sequential([
        keras.layers.Dense(neyron, activation='relu'),
        keras.layers.Dropout(0.2, noise_shape=None, seed=None),
        keras.layers.Dense(neyron * 2, activation='relu'),
        keras.layers.Dropout(0.15, noise_shape=None, seed=None),
        keras.layers.Dense(neyron / 3, activation='relu'),
        keras.layers.Dense(value_tactic, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, Y_train, epochs=500, batch_size=1000, verbose=1, validation_data=(X_test, Y_test))
    score = model.evaluate(XTest, Y_d_test, verbose=0)
    # print("Точность обучения: {0:.2%}".format(score[1]))
    scores.append(score)
    histories.append(history)
model.save("./model")

for scoreItem in scores:
    print("Точность обучения: {0:.2%}".format(scoreItem[1]))
    # print(scoreItem)

# Проверка результата на тестовых данных. Сжатие\нет, С_учителем\Без_учителя зависит от разметки данных и преобразования

fig, axes = plt.subplots(5, 2, figsize=(8, 16))

indexT = 1

for history, [ax1, ax2] in zip(histories, axes):
    plot_history(history, ax1, ax2)
    # plot_history(history, ax1, ax2, './img/' + str(plot_num) + '_model_2_' + '_' + str(indexT) + '_resultImg_.png')
    # plt.savefig('./img/' + str(plot_num) + '_model_2_' + '_' + str(indexT) + '_resultImg_.png', format='png', dpi=600)
    indexT += 1

fig.tight_layout()

predict - strategy - RoboCup / processOkFilte.py

# Программа преобразования данных для предобработки входных данных

import pandas as pd
import numpy as np
from config import resultForPlayerColumn

# teams = ['Gliders2016', 'HELIOS2016']
teams = ['Oxsy', 'HfutEngine2017']

numPeople = 11
gridLen = 6
gridWidth = 4

for item in teams:
    for index in range(numPeople):
        processedDf = pd.read_csv(f'./data/output/{item}_{str(index)}_resultStaticsDf_ok_process.csv', ',')
        processDf = pd.read_csv(f'./data/6x4/{item}_{str(index)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv',
                                ',')
        processDf['strategyOpponent'] = processedDf['strategyOpponent']

        processDf.to_csv(
            f'./data/output6x4/{item}_{str(index)}__resultStaticsDf_ok_process.csv',
            index=False)

predict - strategy - RoboCup / processOutput.py

# Программа преобразования данных для предобработки входных данных 2


import pandas as pd
import numpy as np
from config import resultForPlayerColumn

teams = ['Gliders2016']
teams = ['Oxsy', 'HfutEngine2017']
numPeople = 11


# resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)

def readFile():
    resFlagsTeam = pd.DataFrame(columns=resultForPlayerColumn)
    for item in teams:
        for index in range(numPeople):
            # print(index, './data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv')
            iter = pd.read_csv('./data/output/' + item + '_' + str(index) + '_' + 'resultStaticsDf_ok_process.csv', ',')
            resFlagsTeam = resFlagsTeam.append(iter, ignore_index=True)
    return resFlagsTeam


resFlagsTeam = readFile()

endedDf = pd.DataFrame()


# for indexRow in range(len(resFlagsTeam)):

def getNameColumnIndex(resFlagsTeam: pd.DataFrame, nameColumn: str, indexRow: int, prefix: str):
    testStr = resFlagsTeam.at[indexRow, nameColumn]
    newArrayOpponent = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(np.float)
    newColomn = []
    for index in range(len(newArrayOpponent)):
        newColomn.append(f'{prefix}{index}')
    return newColomn


for indexRow in range(2):
    newArrayOpponentOpponent = getNameColumnIndex(resFlagsTeam, 'opponentVector', indexRow, 'Op')

    testOneMore = pd.Series(resFlagsTeam.iloc[indexRow:indexRow + 1, [0, 1, 2, 3, 4, 5]].squeeze())

    testOneMore = pd.concat([testOneMore, newDf.transpose()], axis=1)
    testStr = resFlagsTeam.at[indexRow, 'teamVector']
    newArrayOpponent = np.array(testStr.replace('[', '').replace(']', '').split(', ')).astype(np.float)
    newColomn = []
    for index in range(len(newArrayOpponent)):
        newColomn.append(f'Tm{index}')
    newDf = pd.DataFrame(data=newArrayOpponent, index=newColomn)
    testOneMore = pd.concat([testOneMore, newDf.transpose()], axis=1, ignore_index=True)

    resFlagsTeam.loc[resFlagsTeam['sideTeam'] == 'left', ('sideTeam')] = 0
    endColumn = resFlagsTeam.iloc[indexRow:indexRow + 1, [8, 9]]
    testOneMore = pd.concat([testOneMore, endColumn], axis=1)
    endedDf.append(testOneMore)
print('test endedDf: ', endedDf)

endedDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(resFlagsTeam)}_withHead.csv',
    index=False)

endedDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(resFlagsTeam)}_withoutHead.csv',
    index=False, header=False)

predict - strategy - RoboCup / getGeneralDfProcess.py

import pandas as pd
import numpy as np

dfNUmber = ['472', '898', '1690']

lenResultDf = 3060
numPeople = 11
gridLen = 6
gridWidth = 4

generalDf = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead_withMerged.csv', ',')

generalDf = generalDf.drop(generalDf[np.isnan(generalDf['yBall']) | np.isnan(generalDf['xBall'])].index)

generalDf = generalDf.drop(
    generalDf[
        (generalDf.yBall > 32.0) |
        (generalDf.yBall < -32.0) |
        (generalDf.xBall > 54.0) |
        (generalDf.xBall < -54.0)
        ].index
)

generalDf.to_csv(
    f'./general_df_process_more_{len(generalDf)}_withHead.csv',
    index=False
)

generalDf.to_csv(
    f'./general_df_process_more_{len(generalDf)}_withoutHead.csv',
    index=False, header=False
)

predict - strategy - RoboCup / getInfo.py

import pandas as pd
import numpy as np
from config import resultForPlayerColumn

rowNum = 13510

resFlagsTeam = pd.read_csv(f'./common_resultStaticsDf_process_more_{rowNum}_list_withZero_head.csv', )


def calcStats(calcDf):
    uniqueStrategy = calcDf['strategyOpponent'].unique()
    dicStatsUnique = {}
    for item in uniqueStrategy:
        dicStatsUnique[item] = len(calcDf[calcDf['strategyOpponent'] == item])
    return dicStatsUnique


stats = calcStats(resFlagsTeam)

newStatsDf = pd.DataFrame()
newStatsDfTest = pd.DataFrame()
limitRow = 4000
limitRowTest = 200

# allowStrategy = ['FrontalAttackGate', 'CenterSideSave', 'UpSideAttack', 'DownCenterSideSave', 'UpCenterSideSave']

# для всех использовать переменную stats
for statistic in stats:
    # print(statistic)
    if (stats[statistic] < limitRow):
        print('drop stats: ', statistic, stats[statistic])
        resFlagsTeam = resFlagsTeam.drop(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].index)
    if (stats[statistic] >= limitRow):
        print('not drop stats: ', statistic, stats[statistic])
        newStatsDf = newStatsDf.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].head(limitRow))
        # print('test len(newStatsDf) - limitRow):', len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]), len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]) - limitRow)
        numTail = len(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic]) - limitRow
        if numTail > 0:
            newStatsDfTest = newStatsDfTest.append(
                resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].tail(limitRowTest))
            # newStatsDfTest = newStatsDfTest.append(resFlagsTeam[resFlagsTeam['strategyOpponent'] == statistic].tail(numTail))

calcStats(newStatsDf)

newStatsDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_list_withZero_head_cropped.csv',
    index=False)

newStatsDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(newStatsDf)}_list_withZero_cropped.csv',
    index=False, header=False)

predict - strategy - RoboCup / generalDfMergeStrategy.py

from config import strategyOnlyList, strategyMergeList

dfNUmber = ['472', '898', '1690']

lenResultDf = 3060
numPeople = 11
gridLen = 6
gridWidth = 4


def calcStats(calcDf):
    uniqueStrategy = calcDf['strategyOpponent'].unique()
    dicStatsUnique = {}
    for item in uniqueStrategy:
        print('strategy', item, len(calcDf[calcDf['strategyOpponent'] == item]))
        dicStatsUnique[item] = len(calcDf[calcDf['strategyOpponent'] == item])
    return dicStatsUnique


generalDfWithMerged = pd.read_csv(f'./general_df_process_more_{lenResultDf}_withHead_withHidden.csv', ',')

stats = calcStats(generalDfWithMerged)

for strategy in strategyMergeList:
    for mergeItem in strategy['valueMerge']:
        query = generalDfWithMerged['strategyOpponent'] == mergeItem

        generalDfWithMerged[query] = generalDfWithMerged[query].assign(strategyOpponent=strategy['value'])

stats = calcStats(generalDfWithMerged)

generalDfWithMerged.to_csv(
    f'./general_df_process_more_{len(generalDfWithMerged)}_withHead_withMerged.csv',
    index=False)

predict - strategy - RoboCup / config.py

teams = ['Gliders2016', 'HELIOS2016']
# teams = ['Oxsy', 'HELIOS2016']
# teams = ['Oxsy', 'HfutEngine2017']
sizeTeam = 11
gridLen = 6
gridWidth = 4
resultForPlayerColumn = [
    'time',
    'x',
    'y',
    'angle',
    'xBall',
    'yBall',
    'opponentVector',
    'teamVector',
    'sideTeam',
    'strategyOpponent'
]
strategyList = [
    {'label': 'Верхняя угловая атака', 'value': 'UpCornerAttack'},
    {'label': 'Нижняя угловая атака', 'value': 'DownCornerAttack'},
    {'label': 'Лобовая атака близи ворот', 'value': 'FrontalAttackNGate'},
    {'label': 'Верхняя боковая атака', 'value': 'UpSideAttack'},
    {'label': 'Нижняя боковая атака', 'value': 'DownSideAttack'},
    {'label': 'Лобовая атака (центр поля)', 'value': 'FrontalAttackGate'},
    {'label': 'Защита верхнего центрального участка', 'value': 'UpCenterSideSave'},
    {'label': 'Защита нижнего центрального участка', 'value': 'DownCenterSideSave'},
    {'label': 'Защита центра поля', 'value': 'CenterSideSave'},
    {'label': 'Защита верхнего угла поля', 'value': 'UpSaveGate'},
    {'label': 'Защита нижнего угла поля', 'value': 'DownSaveGate'},
    {'label': 'Защита от фронтальной атаки', 'value': 'FrontalSaveGate'}
]

strategyOnlyList = [
    'UpCornerAttack',
    'DownCornerAttack',
    'FrontalAttackNGate',
    'UpSideAttack',
    'DownSideAttack',
    'FrontalAttackGate',
    'UpCenterSideSave',
    'DownCenterSideSave',
    'CenterSideSave',
    'UpSaveGate',
    'DownSaveGate',
    'FrontalSaveGate',
]

strategyMergeList = [
    {
        'label': 'Атака вблизи ворот',
        'value': 'NearGateAttack',
        'valueMerge': ['UpCornerAttack', 'DownCornerAttack', 'FrontalAttackNGate']
    },
    {
        'label': 'Атака центра поля',
        'value': 'MiddleFieldAttack',
        'valueMerge': ['UpSideAttack', 'DownSideAttack', 'FrontalAttackGate']
    },
    {
        'label': 'Защита центра поля',
        'value': 'MiddleFieldSave',
        'valueMerge': ['UpCenterSideSave', 'DownCenterSideSave', 'CenterSideSave']
    },
    {
        'label': 'Защита вблизи ворот',
        'value': 'SaveNearGate',
        'valueMerge': ['UpSaveGate', 'DownSaveGate', 'FrontalSaveGate']
    },
]

predict - strategy - RoboCup / additionsMoreRows.py

import pandas as pd
import numpy as np
import random

rowNum = 2836
iterNumber = 4

dfRead = pd.read_csv(f'./general_df_process_more_{rowNum}_withHead.csv', ',')


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
        # print(dfRead[index])
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
        additionalVal = random.randrange(-2, 3, 1)
        if additionalVal < 0 and np.abs(additionalVal) > curVal:
            curVal = np.abs(additionalVal) - curVal
        else:
            curVal += additionalVal
        if curVal < 0:
            curVal = 0
        if curVal != newRow[f'{name}{item}']:
            newRow[f'{name}{item}'] = curVal
    return newRow


newDf = dfRead.copy(deep=True)

for index, row in dfRead.iterrows():
    # if index > 1:
    #     break
    for roundADd in range(iterNumber):
        newRowOp = generateNewRowForAgentTick(row, 'Op', index, roundADd)
        newRowTm = generateNewRowForAgentTick(newRowOp, 'Tm', index, roundADd)

        newDf = newDf.append(newRowTm)

getStatisticSumAgentDf(newDf)

newDf.to_csv(
    f'./common_resultStaticsDf_process_more_{len(newDf)}_withHead_withAddValue.csv',
    index=False)

predict - strategy - RoboCup / mainTest.py

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import numpy as np
from random import randint

# Create a dash application
from config import teams, strategyList, sizeTeam, gridLen, gridWidth

app = dash.Dash(__name__)

global indexTeam
indexTeam = 0
global indexPlayer
indexPlayer = 0
global currentDf
currentDf = None

# REVIEW1: Clear the layout and do not display exforception till callback gets executed
app.config.suppress_callback_exceptions = True

# Application layout
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id='inputTypeStrategy',
                             options=strategyList,
                             placeholder="Стратегии",
                             style={'width': '80%', 'padding': '3px', 'font-size': '20px',
                                    'text-align-last': 'center'}),
                html.Div([
                    html.Button('Разметить', id='submit-val', n_clicks=0,
                                style={'width': '30%', "height": '100%', 'margin-top': '10px'}),
                    html.Button('Сохранить прогресс', id='save-val', n_clicks=0,
                                style={'width': '30%', "height": '100%', 'margin-top': '10px', 'margin-left': '10px'}),
                ])
            ]),
        ]),
        html.Div(id='paragraphOfSize', style={'margin-top': '10px', 'margin-left': '10px', 'font-size': '18px'}),
        html.Img(id='testImg1', style={'width': '100%', "height": '50%', 'border': 'solid 1px black'}),
    ]),

])


class readImageLoopResultI:
    def __init__(self, indexTime, pathToImg):
        self.indexTime = indexTime
        self.pathToImg = pathToImg


class getPathImgResultI:
    def __init__(self, pathToImg, numRow, sideStr):
        self.pathToImg = pathToImg
        self.numRow = numRow
        self.sideStr = sideStr


def readLoopCsv():
    global indexPlayer
    global indexTeam
    global currentDf

    if indexPlayer >= sizeTeam:
        indexTeam += 1
        indexPlayer = 0

    if indexTeam >= len(teams):
        return
        # indexTeam = 0

    nowTeam = teams[indexTeam]

    currentDf = pd.read_csv(f'./data/{nowTeam}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv',
                            ',')
    currentDf['strategyOpponent'] = currentDf['strategyOpponent'].replace(np.nan, '**')

    print(currentDf)


def getPathFromNewImg():
    pathToImg: str = ''
    numRow: int = -1
    sideStr: str = ''
    if not (currentDf.empty):
        for index, row in currentDf.iterrows():
            if row['strategyOpponent'] == '**':
                # indexTime = index
                pathToImg = str(row['time']) + '_' + teams[indexTeam] + '_' + str(
                    indexPlayer) + '_' + 'resultStaticsImg.png'
                numRow = index
                sideStr = row['sideTeam'] + ', Ball: ' + str(row['xBall']) + ' ' + str(row['yBall'])
                break
    return getPathImgResultI(pathToImg, numRow, sideStr)


def saveCurrentProggres(indexNum):
    global indexPlayer
    global indexTeam
    global currentDf
    currentTime = currentDf.at[0 if indexNum == -1 else indexNum, 'time']
    # currentTime = currentDf.at[indexNum, 'time']
    entropyName = randint(1000, 100000)
    currentDf.to_csv(
        f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_{currentTime}_resultStaticsDf_curpr_{str(entropyName)}.csv',
        index=False)


@app.callback(
    [
        Output(component_id="testImg1", component_property='src'),
        Output(component_id="paragraphOfSize", component_property='children'),
        Output(component_id='inputTypeStrategy', component_property='value'),
        Output(component_id='submit-val', component_property='n_clicks'),
        Output(component_id='save-val', component_property='n_clicks')
    ],
    [
        Input(component_id='submit-val', component_property='n_clicks'),
        Input(component_id='save-val', component_property='n_clicks'),
        Input(component_id='inputTypeStrategy', component_property='value')
    ]
)
def processLoop(indexClick, saveClicks, selectStrategy):
    # saveClicks = 0
    global indexPlayer
    global indexTeam
    global currentDf
    initPath = getPathFromNewImg()
    pathToImg = initPath.pathToImg
    indexNum: int = initPath.numRow
    sideStr: str = initPath.sideStr
    if saveClicks > 0:
        saveCurrentProggres(indexNum)
    if not (currentDf.empty) and indexClick > 0 and saveClicks == 0 and selectStrategy != None:
        currentDf.at[indexNum, 'strategyOpponent'] = selectStrategy
        if indexNum == len(currentDf) - 1:
            currentDf.to_csv(
                f'./data/output/{teams[indexTeam]}_{str(indexPlayer)}_resultStaticsDf{str(gridLen)}_{str(gridWidth)}.csv',
                index=False)
            indexPlayer += 1
            readLoopCsv()
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        sideStr = initPath.sideStr
        # print('in if processLoop after',pathToImg, indexNum, currentDf.at[indexNum, 'strategyOpponent'])
        selectStrategy = None
    if indexNum == -1:
        exitIndex = indexNum
        while exitIndex == -1:
            indexPlayer += 1
            readLoopCsv()
            getObj = getPathFromNewImg()
            exitIndex = getObj.numRow
        initPath = getPathFromNewImg()
        pathToImg = initPath.pathToImg
        indexNum = initPath.numRow
        sideStr = initPath.sideStr
    return [
        app.get_asset_url(pathToImg),
        f'Team: {teams[indexTeam]}, {str(indexNum + 1)} из {str(len(currentDf) + 1)}, сторона - {sideStr}',
        selectStrategy,
        0,
        0
    ]


if __name__ == '__main__':
    num = 5 * 7
    print(num)
