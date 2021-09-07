# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn import preprocessing
from pandas.plotting import scatter_matrix

plt.style.use('fivethirtyeight')


def ScatterPlot(df, key1, key2):
  plt.scatter(df[key1], df[key2])
  plt.xlabel(key1)
  plt.ylabel(key2)
  plt.show()


def ScatterPlotAll(df):
  for key1 in df:
    for key2 in df:
      if key1 != key2:
        ScatterPlot(df, key1, key2)


def BarPlot(df, key1, key2):
  plt.bar(df[key1], df[key2])
  plt.xlabel(key1)
  plt.ylabel(key2)
  plt.show()


def BarPlotAll(df):
  for key1 in df:
    for key2 in df:
      if key1 != key2 and str(key1) != 'Name' and str(key2) != 'Name':
        BarPlot(df, key1, key2)


def BoxPlot(df, key1, key2):
  df.boxplot(column=key1, by=key2)
  plt.xlabel(key1)
  plt.ylabel(key2)
  plt.show()


def BoxPlotAll(df):
  for key1 in tolydiniaiDuomenys:
    for key2 in kategoriniaiDuomenys:
      if key1 != key2 and str(key1) != 'Name' and str(key2) != 'Name':
        BoxPlot(df, key1, key2)


def ScatterMatrix():
  sm = scatter_matrix(tolydiniaiDuomenys)
  for ax in sm.ravel():
    ax.set_xlabel(ax.get_xlabel(), fontsize=8, rotation=90)
    ax.set_ylabel(ax.get_ylabel(), fontsize=8, rotation=0)
  plt.show()

def aptiktiEkstremaliasReiksmes(stulpelis):
  outliers = []
  threshold = 4
  mean = stulpelis.mean()
  std = stulpelis.std()

  for reiksme in stulpelis:
    z = (reiksme - mean)/std
    if np.abs(z) > threshold:
      outliers.append(reiksme)
  return outliers

def percentage(part, whole):
  return 100 * float(part) / float(whole)

def histogramos(stulpelis):
  plt.hist(stulpelis, bins=stulpeliuSkaicius(stulpelis.count()), edgecolor='black')
  plt.tight_layout()
  plt.xlabel(stulpelis.name)
  plt.ylabel('Kiekis')
  plt.show()

def stulpeliuSkaicius(n):
  return int(1 + 3.22 * math.log(n,np.e))

attributasColumn = 'Atributo pavadinimas'
kiekisColumn = 'Kiekis (Eilučių sk.)'
trukstamuReiksmiuProcColumn = 'Trūkstamos reikšmės %'
kardinalumasColumn = 'Kardinalumas'
minimaliReiksmeColumn = 'Minimali reikšmė'
maksimaliReiksmeColumn = 'Maksimali reikšmė'
pirmasisKvantilisColumn = '1-asis kvartilis'
treciasisKvantilisColumn = '3-iasis kvartilis'
vidurkisColumn = 'Vidurkis'
medianaColumn = 'Mediana'
standartinisNuokrypisColumn = 'Standartinis nuokrypis'
standartinisNuokrypisColumn = 'Standartinis nuokrypis'

modaColumn = 'Moda'
modaFrequenceColumn = 'Modos dažnumas'
modaPercentageColumn = 'Modos kiekis %'
secondaryModaColumn = '2-oji moda'
secondaryModaFrequenceColumn = '2-os modos dažnumas'
secondaryModaPercentageColumn = '2-os modos kiekis %'

tolydinioTipoLentelesAntrastes = [kiekisColumn, trukstamuReiksmiuProcColumn, kardinalumasColumn, minimaliReiksmeColumn,
                                  maksimaliReiksmeColumn, pirmasisKvantilisColumn, treciasisKvantilisColumn,
                                  vidurkisColumn, medianaColumn, standartinisNuokrypisColumn]
kategorinioTipoLentelesAntrastes = [kiekisColumn, trukstamuReiksmiuProcColumn, kardinalumasColumn, modaColumn,
                                    modaFrequenceColumn, modaPercentageColumn, secondaryModaColumn,
                                    secondaryModaFrequenceColumn, secondaryModaPercentageColumn]
data = pd.read_csv('duomenys.csv', delimiter=',')
tolydinioTipoColumns = list(filter(lambda x: np.issubdtype(data[x].dtype, np.number), data.columns))
kategorinioTipoColumns = list(filter(lambda x: not np.issubdtype(data[x].dtype, np.number), data.columns))

tolydinioTipoLentele = pd.DataFrame(index=tolydinioTipoColumns, columns=tolydinioTipoLentelesAntrastes)
kategorinioTipoLentele = pd.DataFrame(index=kategorinioTipoColumns, columns=kategorinioTipoLentelesAntrastes)
for key in data:
  column = data[key]

  if np.issubdtype(column.dtype, np.number):
    tolydinioTipoLentele.at[key, kiekisColumn] = column.size
    tolydinioTipoLentele.at[key, trukstamuReiksmiuProcColumn] = percentage(column.size - column.count(), column.size)
    tolydinioTipoLentele.at[key, kardinalumasColumn] = column.nunique()
    tolydinioTipoLentele.at[key, minimaliReiksmeColumn] = column.min()
    tolydinioTipoLentele.at[key, maksimaliReiksmeColumn] = column.max()
    tolydinioTipoLentele.at[key, pirmasisKvantilisColumn] = column.quantile(0.25)
    tolydinioTipoLentele.at[key, medianaColumn] = column.quantile(0.5)
    tolydinioTipoLentele.at[key, treciasisKvantilisColumn] = column.quantile(0.75)
    tolydinioTipoLentele.at[key, vidurkisColumn] = column.mean()
    tolydinioTipoLentele.at[key, standartinisNuokrypisColumn] = column.std()
  else:
    kategorinioTipoLentele.at[key, kiekisColumn] = column.size
    kategorinioTipoLentele.at[key, trukstamuReiksmiuProcColumn] = percentage(column.size - column.count(), column.size)
    kategorinioTipoLentele.at[key, kardinalumasColumn] = column.nunique()
    modes = column.mode()
    mode = modes[0]
    secondModes = column[column != mode].mode()
    secondMode = secondModes[0]
    kategorinioTipoLentele.at[key, modaColumn] = mode
    kategorinioTipoLentele.at[key, modaFrequenceColumn] = column[column == mode].size
    kategorinioTipoLentele.at[key, modaPercentageColumn] = percentage(column[column == mode].size, column.size)
    kategorinioTipoLentele.at[key, secondaryModaColumn] = secondModes[0]
    kategorinioTipoLentele.at[key, secondaryModaFrequenceColumn] = column[column == secondMode].size
    kategorinioTipoLentele.at[key, secondaryModaPercentageColumn] = percentage(column[column == secondMode].size,
                                                                               column.size)

#4 Histogramos
tolydiniaiDuomenys = pd.DataFrame(columns=tolydinioTipoColumns)
kategoriniaiDuomenys = pd.DataFrame(columns=kategorinioTipoColumns)
for key in data:
  column = data[key]
  if np.issubdtype(column.dtype, np.number):
    tolydiniaiDuomenys[key] = data[key]
  else:
    kategoriniaiDuomenys[key] = data[key]

for key in tolydiniaiDuomenys:
  #histogramos(data[key])
  pass

#5 Duomenu koregacija
#ekstremalumu salinimas
for key in tolydiniaiDuomenys:
  column = tolydiniaiDuomenys[key]
  ekstremalumai = aptiktiEkstremaliasReiksmes(tolydiniaiDuomenys[key])
  for ekstremalumas in ekstremalumai:
    tolydiniaiDuomenys.loc[(tolydiniaiDuomenys[key] == ekstremalumas), key] = column.mean()

#Tusciu tolydiniu duomenu keitimas vidurkiu
for key in tolydiniaiDuomenys:
  column = tolydiniaiDuomenys[key]
  tolydiniaiDuomenys[key].fillna(column.mean(), inplace=True)

#Tusciu kategoriniu duomenu keitimas moda
for key in kategoriniaiDuomenys:
  column = kategoriniaiDuomenys[key]
  modes = column.mode()
  mode = modes[0]
  kategoriniaiDuomenys[key].fillna(mode, inplace=True)


#6 grafikai
# 6.1
#ScatterPlotAll(tolydiniaiDuomenys)
# 6.2
#ScatterMatrix()
# 6.3
#BarPlotAll(kategoriniaiDuomenys)
# 6.3
#BoxPlotAll(data)


#7 kovariacija ir koreliacija ir koreliacijos matrica pavaizduota grafiskai

tolydinioTipoLentele = tolydinioTipoLentele.apply(pd.to_numeric)
kovariacija = tolydiniaiDuomenys.cov()
koreliacija = tolydiniaiDuomenys.corr()

#kovariacija.to_csv('kovariacija.csv', encoding="utf-8", sep=",")
#koreliacija.to_csv('koreliacija.csv', encoding="utf-8", sep=",")
#print(koreliacija)
#print(kovariacija)

plt.matshow(tolydiniaiDuomenys.corr())
f = plt.figure(figsize=(15, 12))
plt.matshow(tolydiniaiDuomenys.corr(), fignum=f.number)
plt.xticks(range(tolydiniaiDuomenys.shape[1]), tolydiniaiDuomenys.columns, fontsize=14, rotation=45)
plt.yticks(range(tolydiniaiDuomenys.shape[1]), tolydiniaiDuomenys.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
#plt.show()


#8 duomenu normalizacija reziai [0;1]
norm = preprocessing.normalize(tolydiniaiDuomenys, norm='l1')
normalizacija = pd.DataFrame(norm)
#normalizacija.to_csv('normalizacija.csv', encoding="utf-8", sep=",")
print(normalizacija.to_string())

#9 Kategorinio tipo kintamieji keiciami i tolydinio
pakeistaData = data
pakeistaData = pakeistaData.astype(str)

legendary = {'True': 1, 'False': 0}
types = {'Bug': 1, 'Dark': 2, 'Dragon': 3, 'Electric': 4, 'Fairy': 5, 'Fighting': 6, 'Flying': 7, 'Ghost': 8, 'Grass': 9,
         'Ground': 10, 'Ice': 11, 'Normal': 12,'Poison': 13, 'Psychic': 14, 'Rock': 15, 'Steel': 16, 'Water': 17, 'Fire': 18, 'nan':0}
pakeistaData.Legendary = [legendary[item] for item in pakeistaData.Legendary]
pakeistaData['Type1'] = pakeistaData['Type1'].fillna(0)
pakeistaData.Type1 = [types[item] for item in pakeistaData.Type1]
pakeistaData.Type2 = [types[item] for item in pakeistaData.Type2]


pakeistaData['Name'] = pakeistaData.Name.astype('category').cat.rename_categories(range(1, pakeistaData.Name.nunique()+1))

#tolydinioTipoLentele.to_csv('Tolydinio tipo rezultatai.csv', encoding="utf-8", sep=",")
#kategorinioTipoLentele.to_csv('Kategorinio tipo rezultatai.csv', encoding="utf-8", sep=",")