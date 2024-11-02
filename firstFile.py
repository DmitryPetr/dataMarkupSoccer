import pandas as pd
import numpy as np
# import requests
# import datetime
# import os
# import psutil
# from xml.etree import ElementTree
# from lxml import objectify
# import xmltodict, json
# from time import sleep
# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output, State
# import plotly.graph_objects as go
# import plotly.express as px
# from dash import no_update
import folium
from folium import plugins
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv("https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=0&format=csv")
#
# df['Month'] = pd.DatetimeIndex(df['Date']).month
# df = df.groupby(['Month']).mean()
#
# df = df.groupby(['Month']).mean()
# df = df[['Average temperature (°F)', 'Average humidity (%)', 'Average dewpoint (°F)', 'Average barometer (in)', 'Maximum temperature (°F)', 'Minimum temperature (°F)', 'Maximum humidity (%)', 'Minimum humidity (%)', 'Maximum pressure', 'Minimum pressure', 'Maximum windspeed (mph)', 'Maximum gust speed (mph)', 'Maximum heat index (°F)']]
# df = df.transpose()
# df = df[[2,6,8,11]]
# df = df.rename(columns={2:'February', 6:'May', 8:'August', 11:'November'})
# ax = df.plot(kind="barh", stacked=True,  figsize=(20, 14),
#   color=['red', 'royalblue', 'orange','limegreen'])
# ax.legend(labels=["February", "May", "August", "November"])
#
# for p in ax.patches:
#     height = p.get_height()
#     width = p.get_width()
#     x = p.get_x()
#     y = p.get_y()
#     label_text = f'{int(width)}'
#     label_x = x + width -  5
#     label_y = y + height / 2
#
#     ax.text(label_x, label_y, label_text, ha='center', va='center', color="lightgray", fontsize=13)
# df = pd.read_csv('https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=0&format=csv', index_col=[0])
#
# months = ['February', 'May', 'August', 'November']
#
# feb = df[df["Month"] == 2]
# may = df[df["Month"] == 5]
# aug = df[df["Month"] == 8]
# nov = df[df["Month"] == 11]
#
# output = pd.DataFrame()
# columnsSelect = ['Maximum heat index (°F)', 'Maximum gust speed (mph)', 'Maximum windspeed (mph)', 'Minimum pressure', 'Maximum pressure',
# 'Minimum humidity (%)', 'Maximum humidity (%)', 'Minimum temperature (°F)', 'Maximum temperature (°F)', 'Average barometer (in)',
# 'Average dewpoint (°F)', 'Average humidity (%)', 'Average temperature (°F)']
#
# for d in [feb, may, aug, nov]:
#     res = dict()
#     for c in columnsSelect:
#         res[c] = int(np.mean(d[c]))
#     output = output.append(res, ignore_index=True)
#
# # Create new matplotlib chart
# fig, ax = plt.subplots()
# fig.set_size_inches(10,8)
#
# #print(output)
# #print(output.T)
# # Get matplotlib chart
# # output.loc[columnsSelect, []].T.plot.barh(
# #     stacked=True,
# #     color=['darkred', 'royalblue', 'peru','seagreen'],
# #     ax=ax
# # )
# ax = output.T.plot(kind="barh", stacked=True,  figsize=(20, 14),
#   color=['darkred', 'royalblue', 'peru','seagreen'])
#
# # Rename labels
# ax.legend(labels=["February", "May", "August", "November"], fontsize=8)
#
# # Set bar labels
# for rect in ax.patches:
#     # Find where everything is located
#     height = rect.get_height()
#     width = rect.get_width()
#     x = rect.get_x()
#     y = rect.get_y()
#
#     # The height of the bar is the data value and can be used as the label
#     label_text = f'{int(width)}'  # f'{width:.2f}' to format decimal values
#
#     # ax.text(x, y, text)
#     label_x = x + width -  5
#     label_y = y + height / 2
#
#     # only plot labels greater than given width
#     if width > 0:
#         ax.text(label_x, label_y, label_text, ha='center', va='center', color="lightgray", fontsize=8)
#
# fig.tight_layout()

#plt.show()

#df = pd.read_csv('https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=0&format=csv', index_col=[0])
geo_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=413953307&format=csv')
#geo_df = pd.read_csv('data.csv')
world_geo = r'custom.geo.json'
#print(geo_df.tail(10))
#print(geo_df['Country_Region'])
geo_df['Country_Region'].replace(['US'],'United States of America', inplace=True)

world_map = folium.Map(zoom_start=2)

world_map.choropleth(
    geo_data=world_geo,
    data=geo_df,
    columns=['Country_Region', 'Cancers (%)'], # какие из колонок данных мы используем
    key_on='feature.properties.name', # задаем, откуда мы берем название страны в geojson файле
    fill_color='Reds',  # https://colorbrewer2.org/#type=sequential&scheme=Reds&n=3
    fill_opacity=0.7,
    line_opacity=0.2,

)

#
world_map




# for d in [feb, may, aug, nov]:
#     res = dict()
#     for c in d.columns:
#         if c not in columnsSelect:
#           continue
#         if "Date" in c:
#             continue
#         res[c] = math.floor(np.mean(d[c]))
#     output = output.append(res, ignore_index=True)
# print(output)
# #output.to_csv('Faf.csv')
#
# # Create new matplotlib chart
# fig, ax = plt.subplots()
# fig.set_size_inches(10,8)
#
# # Get matplotlib chart
# output.loc[:, output.columns.difference(["Month"])].T.plot.barh(
#     stacked=True,
#     color=['darkred', 'royalblue', 'peru','seagreen'],
#     ax=ax
# )
#
# # Rename labels
# ax.legend(labels=["February", "May", "August", "November"], fontsize=8)
# for container in ax.containers:
#     print(container)
#     ax.bar_label(container, padding=-10, color="lightgray", fontsize=5)
#
# #
# fig.tight_layout()
#
#
# plt.show()

# ax=output.T.plot(
#     kind='barh',
#     stacked=True,
#     color=['darkred', 'royalblue', '#F97306','#008000'],
# )
# # 'orange' #F97306 limegreen #008000
# ax.legend(labels=["February", "May", "August", "November"])
# plt.show()

# ax = output.loc[:, output.columns.difference(["Month"])].transpose().plot.barh(
#     stacked=True,
# figsize=(20, 14),
#     color=['red', 'royalblue', 'orange','limegreen']
# )
#
# ax.legend(labels=["February", "May", "August", "November"])
# plt.show()
















# output.T.plot(
#   kind='barh',
#   stacked=True,
#   figsize=(20, 14),
#   color=['red', 'royalblue', 'orange','limegreen']
# )
# output.transpose().plot(
#     kind='barh',
#     color=['red', 'royalblue', 'orange','limegreen'],
#     figsize=(20, 14),
#     stacked=True # Значение не накапливается
# )
# plt.xlabel('Продолжительность жизни')
# plt.ylabel('Год')
# title = plt.title('Продолжительность жизни в Японии, Кении, РФ')
#plt.show()












# feb = df[df["Month"] == 2]
# may = df[df["Month"] == 5]
# aug = df[df["Month"] == 8]
# nov = df[df["Month"] == 11]

#newDf = pd.DataFrame()

#newDf['Maximum heat index (°F)'] = df.

#print(df_start.columns)

# df['Month'].replace({2: 'February', 5: 'May', 8: 'August', 11: 'November'})
# print(df['Month'])


# columnsSelect = ['Maximum heat index (°F)', 'Maximum gust speed (mph)', 'Maximum windspeed (mph)', 'Minimum pressure', 'Maximum pressure',
# 'Minimum humidity (%)', 'Maximum humidity (%)', 'Minimum temperature (°F)', 'Maximum temperature (°F)', 'Average barometer (in)',
# 'Average dewpoint (°F)', 'Average humidity (%)', 'Average temperature (°F)']
# columnsSelect = ['Month', 'Maximum heat index (°F)', 'Maximum gust speed (mph)', 'Maximum windspeed (mph)', 'Minimum pressure', 'Maximum pressure',
# 'Minimum humidity (%)', 'Maximum humidity (%)', 'Minimum temperature (°F)', 'Maximum temperature (°F)', 'Average barometer (in)',
# 'Average dewpoint (°F)', 'Average humidity (%)', 'Average temperature (°F)']
#newDf = pd.DataFrame(columns=columnsSelect)

#newDf['Month']
# print(newDf)
# for d in [feb, may, aug, nov]:
#     res = []
#     for c in columnsSelect:
#         if "Month" in c:
#             continue
#         res.append(np.mean(d[c]))
#         #print(res)
#         # if c in columnsSelect:
#         #     res.append(np.mean(d[c]))
#     #print(d['Month'])
#     print(res)
#     newDf.append(res, ignore_index=True)
# print(newDf)
        #res[c] = np.mean(d[c])
# columnsSelect = ['Month', 'Maximum heat index (°F)', 'Maximum gust speed (mph)', 'Maximum windspeed (mph)', 'Minimum pressure', 'Maximum pressure',
# 'Minimum humidity (%)', 'Maximum humidity (%)', 'Minimum temperature (°F)', 'Maximum temperature (°F)', 'Average barometer (in)',
# 'Average dewpoint (°F)', 'Average humidity (%)', 'Average temperature (°F)']
#newDf = pd.DataFrame()
#print(newDf)

#test = input()
# C++
# 1. Найти сумму N чисел натурального ряда кратных 11, начиная с K>0. N>0 N вводится с клавиатуры

# train = pd.read_csv('https://docs.google.com/spreadsheets/d/1VSZqGFuDI9ebuBdSLPcy8Gyi9085eLuLnn9Kou7Ao6U/export?gid=1501399475&format=csv', index_col=[0])

# N = 0
# K = 0
# sum = 0
#
# print("Enter N > 0 (example: 10) ",  N, K)
# N = int(input())
# print("Enter K > 0 (example: 2) ",  N, K)
# K = int(input())
#
# if (N > 0 and K > 0):
#     for iter in range(K, N+1, 1):
#         if (iter % 11 == 0):
#             sum += 1
#     print("Sum: ", sum)
# else:
#     print("N or/and K less 0: ", N, " ", K)


# path = '\\20170904132709-Gliders2016_0-vs-HELIOS2016_0-Gliders2016_1-moving.csv'
# train = pd.read_csv('C:\qualifyingWork\example_csv\\20170904132709-Gliders2016_0-vs-HELIOS2016_0-Gliders2016_1-moving.csv', ';')
#
# print(train)
# print(train['# time'])

# train_X = Dogs_n_Cats.drop(['num'], axis=1)
# train_Y = Dogs_n_Cats.num
#
# clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=7)

#pd.options.display.max_columns = 10
#print(Songs.head())

# train = pd.read_csv('https://docs.google.com/spreadsheets/d/1VSZqGFuDI9ebuBdSLPcy8Gyi9085eLuLnn9Kou7Ao6U/export?gid=1501399475&format=csv', index_col=[0])
#
# print(len(train[(train['Цена'] > 10) & (train['Гликемический индекс'] % 2 == 0)]))

# mse_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1VSZqGFuDI9ebuBdSLPcy8Gyi9085eLuLnn9Kou7Ao6U/export?gid=0&format=csv', index_col=[0])
#
# print(mse_df.rename(columns={x : int(x) for x in mse_df.columns}, inplace=True))
#
# response = requests.get("http://worldtimeapi.org/api/timezone/Europe/Moscow")
# dateCurrent = response.json()['datetime']
# epoch = datetime.datetime.utcfromtimestamp(0)
#
# def unix_time_millis(dt):
#     return (dt - epoch).total_seconds() * 1000.0
#
# date_time_obj = datetime.datetime.strptime(dateCurrent[ 0:len(dateCurrent)-6], '%Y-%m-%dT%H:%M:%S.%f')
# print('datetime.datetime.now()', date_time_obj, datetime.datetime.now(), unix_time_millis(date_time_obj)-unix_time_millis(datetime.datetime.now()))
# print(response.elapsed.total_seconds())

# print(psutil.disk_partitions())
# disks = psutil.disk_partitions()
# for item in disks:
#     print(item.mountpoint)
#
# response = requests.get('http://www.cbr.ru/scripts/XML_val.asp?d=0')
#
# print(response.content)
#
# pp = xmltodict.parse(response.content)
# print(json.dumps(pp))
# picdic = json.loads(json.dumps(pp))
# picdicValuta = picdic['Valuta']
# itsDollaR = "R01235"
# print(picdicValuta['Item'])
#
# while True:
#     for item in picdicValuta['Item']:
#         if item['@ID']==itsDollaR:
#             print(item["Nominal"], "ЕТО ВАША ХУЙНЯ?")
#             break
#     sleep(60)

# main = objectify.fromstring(response.content)
# # main.object1[0]             # content
# # main.object1[1]             # contenbar
# # main.object1[0].get("attr") # name
# # main.test                   # me
#
# print('main ', main)

# tree = ElementTree.fromstring(response.content)
#
# for item in tree:
#     print(item)








#mse_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1VSZqGFuDI9ebuBdSLPcy8Gyi9085eLuLnn9Kou7Ao6U/export?gid=1385166020&format=csv', index_col=[0])
#print(mse_df)

### Задание.
### Измените значения, которые хранятся в столбцах "Градусы","Влажность", так, чтобы в них хранились числа (без лишних данных).
### Значения nan замените средним по столбцу. Измените название столбца "Ветер" на "Ветер (м/с)"
# https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/edit#gid=2051993671
# df = pd.read_csv('https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=2051993671&format=csv', header=6, index_col=0, skipfooter=1, engine='python', usecols=['Город', 'Градусы',  "Влажность", "Давление", "Ветер"])
# df = pd.read_csv('https://docs.google.com/spreadsheets/d/1P3qaDaoPoRTkITh3M8uCMVfYAnn5pl7tMlRhYh9eGNw/export?gid=2051993671&format=csv', index_col="enrollee_id")
# df.dropna(inplace=True)
# df = df['training_hours'].astype(float)
# female_count = len(df[(df["gender"] == "Female") & (df["training_hours"] > 20)])
# male_count = len(df[(df["gender"] == "Male") & (df["training_hours"] < 10)])
# df['experience'] = df['experience'].str.replace('[!<>]','', regex=True).astype(float)
# df = df.sort_values(by=['city_development_index'])
#
# # print(female_count)
# # print(male_count)
#
# print(df)
# df['Ветер'] = df['Ветер'].str.replace('[!м/с]', '', regex=True).astype(int)
# df['Градусы'] = df['Градусы'].str.replace('[°]', '', regex=True)
# #df['Влажность'] = df['Влажность'].str.replace('[!%*]', '', regex=True)
# df['Влажность'] = df['Влажность'].str.replace('[^0-9]', '', regex=True).astype(float)
# df['Давление'] = df['Давление'].str.replace('[ м]', '', regex=True)
# df = df.rename(columns={'Ветер': 'Ветер м/с'})
# df = df.fillna(df.mean())
# print(df)
# print(df.mean())
# #print(df['Влажность'])
































# X_test = pd.read_json('F:/info/dataset_209691_15 (1).txt')
# train_C_D_X = Dogs_n_Cats.drop(['Вид'], axis=1)
# train_C_D_Y = Dogs_n_Cats.Вид
#
# data_score = pd.DataFrame()
# max_depth_mas = range(1, 100)
#
#
# clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=7)
# clf.fit(train_C_D_X, train_C_D_Y)
# #cross_val_score(clf, train_C_D_X, train_C_D_Y, cv=5)
#
#
# hh = clf.predict(X_test)
# l = list(hh)
# l.count('собачка')
#
# print(l.count('собачка'))


# for max_depth in max_depth_mas:
#     clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=max_depth)
#     #clf.fit(train_iris_X, train_iris_Y)
# txt
#     cross_val = cross_val_score(clf, train_C_D_X, train_C_D_Y, cv=5).mean()
#
#
#     tmp_score_data = pd.DataFrame({'max_depth': [max_depth],
#                                        'cross_val': [cross_val]
#                                        })
#     data_score = data_score.append(tmp_score_data)
#
#     data_score_long = pd.melt(data_score, id_vars=['max_depth'], value_vars=['cross_val'],
#                               var_name='set_type', value_name='score')
#
# sns.lineplot(x='max_depth', y='score', hue='set_type', data=data_score_long)
# plt.show();

#print(data_score_long.head())
# print(train_C_D_X)
# print(train_C_D_Y)



























#events_train = pd.read_csv('F:/info/event_data_train.csv')
# train_iris = pd.read_csv('F:/info/train_iris.csv')
# test_iris = pd.read_csv('F:/info/test_iris.csv')
#
# max_val_deep = range(1, 100)
# train_iris_X = train_iris.drop(['species'], axis=1)
# train_iris_Y = train_iris.species
#
# test_iris_X = test_iris.drop(['species'], axis=1)
# test_iris_Y = test_iris.species
#
# # print(train_iris_X.head())
# # print(train_iris_Y.head())
# data_score = pd.DataFrame()
#
# for max_depth in max_val_deep:
#     np.random.seed(0)
#     clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth= max_depth)
#     clf.fit(train_iris_X, train_iris_Y)
#     train_score = clf.score(train_iris_X, train_iris_Y)
#     test_score = clf.score(test_iris_X, test_iris_Y)
#
#     tmp_score_data = pd.DataFrame({'max_depth': [max_depth],
#                                    'train_score': [train_score],
#                                    'test_score' : [test_score]
#                                    })
#     data_score = data_score.append(tmp_score_data)
#
# data_score_long = pd.melt(data_score, id_vars=['max_depth'], value_vars=['train_score', 'test_score'],
#                           var_name='set_type', value_name='score')
#
# sns.lineplot(x='max_depth', y='score', hue='set_type', data=data_score_long)
#
# plt.show();

#print(data_score.head())













# events_train = events_train.head(1150000)
# events_train['date'] = pd.to_datetime(events_train.timestamp, unit='s')
# events_train['month'] = events_train.date.dt.month
# events_train['year'] = events_train.date.dt.year
# events_train = events_train.drop(columns=['date', 'timestamp'])
# #events_train = events_train.loc[(events_train.year <= 2016)]
# events_train = events_train.drop_duplicates(subset=['user_id', 'month'])
# events_train = events_train.drop(columns=['step_id', 'year'])
# events_train = events_train.groupby(['user_id']).nunique()
# events_train = events_train.loc[(events_train.month >= 9)]
# print(events_train)


# events_train_id_or_act = events_train[['user_id', 'action']]
# print(events_train_id_or_act)
#submissions_train = pd.read_csv('F:/info/submissions_data_train.csv')
#tmp = events_train.groupby(['action', 'user_id']).nunique()
#print(tmp)
#print(events_train)
#print(submissions_train)


#my_stat = pd.read_csv('F:/info/my_stat.csv')
# my_stat = my_stat.rename(columns = {'V1':'session_value', 'V2':'group', 'V3':'time', 'V4':'n_users'})
# tmp = my_stat.groupby('group', as_index=False).agg({'session_value': 'mean'}).rename(columns = {'session_value':'mean_session_value'})
# mean_session_value_data = pd.DataFrame(data=tmp)
# print(mean_session_value_data)

#my_stat = my_stat.fillna(0)
# med = my_stat.loc[my_stat.n_users >= 0.0]
# #print(my_stat.n_users)
# #print(med['n_users'].median())
# test = my_stat
# #print(my_stat.mask(my_stat['n_users'] > 0, med['n_users'].median()))
# my_stat.loc[my_stat['n_users'] < 0, 'n_users'] = med['n_users'].median()
# print(test)
#tmp = my_stat.where(my_stat.n_users > 0, med['n_users'].median())
#print(tmp)













#data = {'type': ['A', 'A', 'B','B'], 'value': [10, 14,12,23]}
#df = pd.DataFrame(data=data)
#df = pd.read_csv("F:/info/iris.csv")
#tmp = my_stat[my_stat.n_users >= 0.0].n_users

#tmp = my_stat.rename(columns = {'V1':'session_value', 'V2':'group', 'V3':'time', 'V4':'n_users'})
#subset_1 = my_stat.assign(V5 = my_stat.V1+my_stat.V4, V6 = np.log(my_stat.V2))
#print(my_stat)
#ax = sns.pairplot(df)
# plt.figure(figsize=(50,50))
# for column in df:
#     sns.distplot(df[column],  kde_kws={"label":column})
#plt.show();

#теплокарты
# df = pd.read_csv("F:/info/genome_matrix.csv")
# print(df)
# sns.set()
# genome = pd.read_csv('F:/info/genome_matrix.csv', index_col=0)
# print(genome)
# g = sns.heatmap(genome, cmap='viridis')
# g.xaxis.set_ticks_position('top')
# g.xaxis.set_tick_params(rotation=90)
# plt.show();

#df.plot.scatter(x='x',y='y')
#sns.scatterplot(df.iloc[:, 0], df.iloc[:, 1])
#plt.show();
#print(concentrations.filter(like=''))
#alaninN = concentrations.groupby(["genus", 'alanin']).nunique()
#alaninN = concentrations.groupby(["group", 'glucose']).describe()
#print(alaninN)
#alaninN = alaninN.loc[:,'alanin']
#print(alaninN.describe())
#print(alaninN.mean())
#alanin = alaninN.loc['Fucus']
#print(alanin)
#print(concentrations.groupby('genus').describe())


#print(Money.groupby(['Type', 'Executor']).aggregate({'Salary': 'mean'}))
#print(Dota_Hero.groupby(['attack_type', 'primary_attr']).nunique())
#al = Dota_Hero.groupby("legs").nunique()
# var1 = students_Perfomance.loc[students_Perfomance.lunch == 'free/reduced']
# var2 = students_Perfomance.loc[students_Perfomance.lunch == 'standard']
# print(var1.describe())
# print('\n\n\n')
# print(var2.describe())