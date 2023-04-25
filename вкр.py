# -*- coding: utf-8 -*-
"""ВКР

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M2XhmMRtMMFb19Uqbi843YyTjBXw2UV9

I. Предобработка данных

Импорт библиотек
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

x_bp = pd.read_excel('/content/drive/MyDrive/X_bp.xlsx', index_col=0)
x_bp

x_bp.head()



x_bp.info()

x_nup = pd.read_excel('/content/drive/MyDrive/X_nup.xlsx', index_col=0)
x_nup

x_nup.head()

x_nup.info()

df1 = x_bp.merge(x_nup, how = 'inner', left_index = True, right_index = True)
df1

df1['Угол нашивки, град'].nunique()

"""Так как кол-во уникальных значений в колонке Угол нашивки равно 2, можем привести данные в этой колонке к значениям 0 и 1
Проверим кол-во элементов, где Угол нашивки равен 0 градусов
"""

df1['Угол нашивки, град'][df1['Угол нашивки, град'] == 0.0].count()

df = df1.copy()

df = df.replace({'Угол нашивки, град': {0.0 : 0, 90.0 : 1}})
df['Угол нашивки, град'] = df['Угол нашивки, град'].astype(int)

df = df.rename(columns={'Угол нашивки, град' : 'Угол нашивки'})

df['Угол нашивки'][df['Угол нашивки'] == 0].count()

"""После преобразования колонки Угол нашивки к значениям 0 и 1, кол-во элементов, где угол нашивки равен 0 не изменилось (520 до и после преобразования)"""

df.tail()

df.duplicated().sum()

df.isnull().sum()

df.info()

df.index = df.index.astype('int')

df.head()

df.describe()

sns.set_style('darkgrid')
sns.pairplot(df, hue = 'Угол нашивки', markers=["o", "s"], diag_kind= 'auto', palette='Set2')

"""Попарные графики рассеяния точек не показывают какой-либо зависимости между данными

Есть выбросы??
"""

df.columns

a = 5
b = 5
c = 1

plt.figure(figsize=(35,35))

for col in df.columns:
    plt.subplot(a, b, c)
    plt.figure(figsize=(7,5))
    sns.histplot(data = df[col], kde=True)
    plt.ylabel(None)
    plt.title(col, size = 20)
    plt.show()
    c+=1

'''
for col in df.columns:
    plt.figure(figsize=(10,5))
    plt.title('Гистограмма:'+ ' ' + col)
    plt.ylabel('Количество элементов')
    sns.histplot(data = df[col], kde=True)
    plt.show()
    print(f'Минимальное значение: {df[col].min().round(3)}')
    print(f'Максимальное значение: {df[col].max().round(3)}')
    print(f'Среднее значение: {df[col].mean().round(3)}')
    print(f'Медианное значение: {df[col].median().round(3)}')
'''

import scipy
accepted_list = []
rejected_list = []

for col in df.columns:
    alpha = 0.05
    stat, p = scipy.stats.normaltest(df[col]) # Критерий согласия Пирсона
    print('Statistics=%.3f, p-value=%.3f' % (stat, p))
    if p > alpha:
        accepted_list.append(col)
    else:
        rejected_list.append(col)
print(f'Наименование колонок с данными С нормальным распределением: {accepted_list}')
print(f'Наименование колонок с данными БЕЗ нормального распределения : {rejected_list}')

a = 5
b = 5
c = 1

plt.figure(figsize=(35,35))

for col in df.columns:
    plt.subplot(a, b, c)
    #plt.figure(figsize=(7,5))
    sns.boxplot(data = df, y=df[col], fliersize=15, linewidth=5)
    plt.ylabel(None)
    plt.title(col, size = 20)
    #plt.show()
    c+=1

mask = np.triu(df.corr())
f, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(df.corr(), mask=mask, annot=True, square=True, cmap='coolwarm')
plt.xticks(rotation=45, ha='right')
plt.show()

"""Максимальная корреляция между Плотностью нашивки и углом нашивки и составляет 0.11, что говорит об отсутствии зависимости между этими данными. Корреляция между всеми параметрами очень близка к 0, что говорит об отсутствии корреляционных связей между переменными.

Очистим данные от выбросов
"""

for col in df.columns:
    q75,q25 = np.percentile(df.loc[:,col],[75,25])
    intr_qr = q75-q25

    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)

    df.loc[df[col] < min,col] = np.nan
    df.loc[df[col] > max,col] = np.nan

df.isnull().sum()

"""Выбросов не так много, можно их удалить"""

df = df.dropna(axis=0)

df.isnull().sum()

df.info()

a = 5
b = 5
c = 1

plt.figure(figsize=(35,35))

for col in df.columns:
    plt.subplot(a, b, c)
    #plt.figure(figsize=(7,5))
    sns.boxplot(data = df, y=df[col], fliersize=15, linewidth=5)
    plt.ylabel(None)
    plt.title(col, size = 20)
    #plt.show()
    c+=1

'''
for col in df.columns:
    plt.figure(figsize=(7,5))
    sns.boxplot(data = df, y=df[col])
    plt.title(col)
    plt.show()
    print(f'Минимальное значение: {df[col].min().round(3)}')
    print(f'Максимальное значение: {df[col].max().round(3)}')
    print(f'Среднее значение: {df[col].mean().round(3)}')
    print(f'Медианное значение: {df[col].median().round(3)}')
'''

"""Нормальзуем значения с помощью метода MinMaxScaler"""

from sklearn.preprocessing import MinMaxScaler

min_max_scaler = MinMaxScaler()
df_norm = pd.DataFrame(min_max_scaler.fit_transform(df), columns = df.columns, index=df.index)

df_norm.describe()

sns.pairplot(df_norm, hue = 'Угол нашивки', markers=["o", "s"], diag_kind= 'auto', palette='Set2')

mask = np.triu(df_norm.corr())
f, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(df_norm.corr(), mask=mask, annot=True, square=True, cmap='coolwarm')
plt.xticks(rotation=45, ha='right')
plt.show()

"""II. Построение моделей для прогноза модуля упругости при растяжении и прочности при растяжении"""

from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

"""Разбиваем данные на обучающую и тестовую выборки"""

x_upr = df.drop(['Модуль упругости при растяжении, ГПа'], axis=1)
x_pr = df.drop(['Прочность при растяжении, МПа'], axis=1)
y_upr = df[['Модуль упругости при растяжении, ГПа']]
y_pr = df[['Прочность при растяжении, МПа']]

X_train_upr, X_test_upr, y_train_upr, y_test_upr = train_test_split(x_upr, y_upr, test_size=0.3, random_state=1)
X_train_pr, X_test_pr, y_train_pr, y_test_pr = train_test_split(x_pr, y_pr, test_size=0.3, random_state=1)

"""Метод К ближайших соседей"""

knr = KNeighborsRegressor()
knr_params = {'n_neighbors' : range(1, 301, 2), 
          'weights' : ['uniform', 'distance'],
          'algorithm' : ['auto', 'ball_tree', 'kd_tree', 'brute']
          }
GSCV_knr_upr = GridSearchCV(knr, knr_params, n_jobs=-1, cv=10)
GSCV_knr_upr.fit(X_train_upr, y_train_upr)
GSCV_knr_upr.best_params_

knr_upr = GSCV_knr_upr.best_estimator_
print(f'R2-score KNR для модуля упругости при растяжении: {knr_upr.score(X_test_upr, y_test_upr).round(3)}')

models = pd.DataFrame()

knr_upr_result = pd.DataFrame({
   'Model': 'KNeighborsRegressor_upr', 
   'MAE': mean_absolute_error(y_test_upr, knr_upr.predict(X_test_upr)), 
   'R2 score': knr_upr.score(X_test_upr, y_test_upr).round(3)
}, index=['Модуль упругости при растяжении'])

models = pd.concat([models, knr_upr_result])

"""Если коэффициент детерминации=0, это значит, что модель прогнозирует данные с таким же результатом, как если бы мы всегда брали среднее значение прогнозируемой переменной"""

GSCV_knr_pr = GridSearchCV(knr, knr_params, n_jobs=-1, cv=10)
GSCV_knr_pr.fit(X_train_pr, y_train_pr)
GSCV_knr_pr.best_params_

knr_pr = GSCV_knr_pr.best_estimator_
print(f'R2-score KNR для прочности при растяжении: {knr_pr.score(X_test_pr, y_test_pr).round(3)}')

knr_pr_result = pd.DataFrame({
   'Model': 'KNeighborsRegressor_pr', 
   'MAE': mean_absolute_error(y_test_pr, knr_pr.predict(X_test_pr)), 
   'R2 score': knr_pr.score(X_test_pr, y_test_pr).round(3)
}, index=['Прочность при растяжении'])

models = pd.concat([models, knr_pr_result])

"""Стохастический градиентный спуск"""

sgd = SGDRegressor()
sgd_params = {'loss' : ['squared_error', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'], 
          'penalty' : ['elasticnet', 'l2', 'l1'],
          'alpha' : [0.0001, 0.001, 0.01, 0.0002, 0.002],
          'learning_rate' : ['optimal', 'invscaling', 'adaptive'],
          'epsilon' : [0.1, 0.01, 0.2, 0.02]
          }
GSCV_sgd_upr = GridSearchCV(sgd, sgd_params, cv=10, verbose=0)
GSCV_sgd_upr.fit(X_train_upr, np.ravel(y_train_upr))
GSCV_sgd_upr.best_params_

sgd_upr = GSCV_sgd_upr.best_estimator_
print(f'R2-score KNR для модуля упругости при растяжении: {sgd_upr.score(X_test_upr, y_test_upr).round(3)}')
print(mean_absolute_error(y_test_upr, sgd_upr.predict(X_test_upr)))

sgd_upr_result = pd.DataFrame({
   'Model': 'SGDRegressor_upr', 
   'MAE': mean_absolute_error(y_test_upr, sgd_upr.predict(X_test_upr)), 
   'R2 score': sgd_upr.score(X_test_upr, y_test_upr).round(3)
}, index=['Модуль упругости при растяжении'])

models = pd.concat([models, sgd_upr_result])

GSCV_sgd_pr = GridSearchCV(sgd, sgd_params, cv=10)
GSCV_sgd_pr.fit(X_train_pr, np.ravel(y_train_pr))
GSCV_sgd_pr.best_params_

sgd_pr = GSCV_sgd_pr.best_estimator_
print(f'R2-score KNR для модуля упругости при растяжении: {sgd_pr.score(X_test_pr, y_test_pr).round(3)}')
print(mean_absolute_error(y_test_pr, sgd_pr.predict(X_test_pr)))

sgd_pr_result = pd.DataFrame({
   'Model': 'SGDRegressor_pr', 
   'MAE': mean_absolute_error(y_test_pr, sgd_pr.predict(X_test_pr)), 
   'R2 score': sgd_pr.score(X_test_pr, y_test_pr).round(3)
}, index=['Прочность при растяжении'])

models = pd.concat([models, sgd_pr_result])

"""Если R2<0, это значит, что разработанная модель даёт прогноз даже хуже, чем простое усреднение.

Линейная регрессия
"""

lr = LinearRegression()
lr_params = {
    'fit_intercept': [True, False]
}
GSCV_lr_upr = GridSearchCV(lr, lr_params, n_jobs=-1, cv=10)
GSCV_lr_upr.fit(X_train_upr, y_train_upr)
GSCV_lr_upr.best_params_

lr_upr = GSCV_lr_upr.best_estimator_
print(f'R2-score LR для модуля упругости при растяжении: {lr_upr.score(X_test_upr, y_test_upr).round(3)}')

lr_upr_result = pd.DataFrame({
   'Model': 'LinearRegression_upr', 
   'MAE': mean_absolute_error(y_test_upr, lr_upr.predict(X_test_upr)), 
   'R2 score': lr_upr.score(X_test_upr, y_test_upr).round(3)
}, index=['Модуль упругости при растяжении'])

models = pd.concat([models, lr_upr_result])

GSCV_lr_pr = GridSearchCV(lr, lr_params, n_jobs=-1, cv=10)
GSCV_lr_pr.fit(X_train_pr, y_train_pr)
GSCV_lr_pr.best_params_

lr_pr = GSCV_lr_pr.best_estimator_
print(f'R2-score LR для прочности при растяжении: {lr_pr.score(X_test_pr, y_test_pr).round(3)}')

lr_pr_result = pd.DataFrame({
   'Model': 'LinearRegression_pr', 
   'MAE': mean_absolute_error(y_test_pr, lr_pr.predict(X_test_pr)), 
   'R2 score': lr_pr.score(X_test_pr, y_test_pr).round(3)
}, index=['Прочность при растяжении'])

models = pd.concat([models, lr_pr_result])

"""Случайный лес"""

rfr = RandomForestRegressor()
rfr_params = {
    'n_estimators' : range(10, 1000, 10),
    'criterion' : ['squared_error', 'absolute_error', 'poisson'],
    'max_depth' : range(1, 7),
    'min_samples_split' : range(20, 50, 5),
    'min_samples_leaf' : range(2, 8),
    'bootstrap' : [True, False]
}
RSCV_rfr_upr = RandomizedSearchCV(rfr, rfr_params, n_jobs=-1, cv=10, verbose=4)
RSCV_rfr_upr.fit(X_train_upr, np.ravel(y_train_upr))
RSCV_rfr_upr.best_params_

rfr_upr = RSCV_rfr_upr.best_estimator_
print(f'R2-score RFR для модуля упругости при растяжении: {rfr_upr.score(X_test_upr, y_test_upr).round(3)}')

rfr_upr_result = pd.DataFrame({
   'Model': 'RandomForestRegressor_upr', 
   'MAE': mean_absolute_error(y_test_upr, rfr_upr.predict(X_test_upr)), 
   'R2 score': rfr_upr.score(X_test_upr, y_test_upr).round(3)
}, index=['Модуль упругости при растяжении'])

models = pd.concat([models, rfr_upr_result])

RSCV_rfr_pr = RandomizedSearchCV(rfr, rfr_params, n_jobs=-1, cv=10, verbose=4)
RSCV_rfr_pr.fit(X_train_pr, np.ravel(y_train_pr))
RSCV_rfr_pr.best_params_

rfr_pr = RSCV_rfr_pr.best_estimator_
print(f'R2-score RFR для прочности при растяжении: {rfr_pr.score(X_test_pr, y_test_pr).round(3)}')

rfr_pr_result = pd.DataFrame({
   'Model': 'RandomForestRegressor_pr', 
   'MAE': mean_absolute_error(y_test_pr, rfr_pr.predict(X_test_pr)), 
   'R2 score': rfr_pr.score(X_test_pr, y_test_pr).round(3)
}, index=['Прочность при растяжении'])

models = pd.concat([models, rfr_pr_result])

"""Модели не справляются с решением поставленной задачи, попробуем с помощью многослойного перцептрона из библиотеки sklearn"""

from sklearn.neural_network import MLPRegressor

mlpr = MLPRegressor(random_state=2)
mlpr_params = {
    'hidden_layer_sizes' : [(64, 32, 12), (12, 12, 12, 12, 12),
                            (32, 32, 16, 8), (16, 16, 8)],
    'activation' : ['identity', 'logistic', 'tanh', 'relu'],
    'solver' : ['sgd', 'adam'],
    'max_iter' : [300],
    'learning_rate' : ['constant', 'adaptive', 'invscaling']
}

GSCV_mlpr_upr = GridSearchCV(mlpr, mlpr_params, n_jobs=-1, cv=10)
GSCV_mlpr_upr.fit(X_train_upr, np.ravel(y_train_upr))
GSCV_mlpr_upr.best_params_

mlpr_upr = GSCV_mlpr_upr.best_estimator_
print(f'R2-score MLPR для модуля упругости при растяжении: {mlpr_upr.score(X_test_upr, y_test_upr).round(3)}')

mlpr_upr_result = pd.DataFrame({
   'Model': 'MLPRegressor_upr', 
   'MAE': mean_absolute_error(y_test_upr, mlpr_upr.predict(X_test_upr)), 
   'R2 score': mlpr_upr.score(X_test_upr, y_test_upr).round(3)
}, index=['Модуль упругости при растяжении'])

models = pd.concat([models, mlpr_upr_result])

GSCV_mlpr_pr = GridSearchCV(mlpr, mlpr_params, n_jobs=-1, cv=10)
GSCV_mlpr_pr.fit(X_train_pr, np.ravel(y_train_pr))
GSCV_mlpr_pr.best_params_

mlpr_pr = GSCV_mlpr_pr.best_estimator_
print(f'R2-score MLPR для прочности при растяжении: {mlpr_pr.score(X_test_pr, y_test_pr).round(3)}')

mlpr_pr_result = pd.DataFrame({
   'Model': 'MLPRegressor_pr', 
   'MAE': mean_absolute_error(y_test_pr, mlpr_pr.predict(X_test_pr)), 
   'R2 score': mlpr_pr.score(X_test_pr, y_test_pr).round(3)
}, index=['Прочность при растяжении'])

models = pd.concat([models, mlpr_pr_result])

models_sort = models.sort_values(by=['MAE', 'R2 score'])
models_sort

sns.catplot(data=models_sort[0:5], x='Model', y='MAE', kind='bar', height=6, aspect=2)
plt.ylim(ymin=2.4, ymax=3.4)
plt.xticks(size=12)
plt.title('Средняя абсолютная ошибка моделей прогноза Модуля упругости при растяжении, ГПа', size=15)

sns.catplot(data=models_sort[5:10], x='Model', y='MAE', kind='bar', height=6, aspect=2)
plt.ylim(ymin=360, ymax=390)
plt.xticks(size=12)
plt.title('Средняя абсолютная ошибка моделей прогноза Прочности при растяжении, МПа', size=15)

"""3. Построение нейронной сети на Keras для предсказания Модуля упругости при растяжении, Прочности при растяжении, Соотношения матрица-наполнитель"""

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, LeakyReLU, Activation, Dropout, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint

print(tf.__version__)

"""Нейронная сеть для прогноза модуля упругости при растяжении"""

normalizer = tf.keras.layers.Normalization(axis=-1)

X_train_upr_norm = normalizer.adapt(np.array(X_train_upr))

model_upr = Sequential(X_train_upr_norm)

model_upr.add(Dense(128))
model_upr.add(BatchNormalization())
model_upr.add(LeakyReLU())
model_upr.add(Dense(64))
model_upr.add(BatchNormalization())
model_upr.add(LeakyReLU())
model_upr.add(Dense(64))
model_upr.add(BatchNormalization())
model_upr.add(LeakyReLU())
model_upr.add(Dense(32))
model_upr.add(BatchNormalization())
model_upr.add(LeakyReLU())
model_upr.add(Dense(32))
model_upr.add(BatchNormalization())
model_upr.add(LeakyReLU())
model_upr.add(Dense(1))
model_upr.add(Activation(activation='elu'))

model_upr.compile(
    optimizer=tf.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=False),
    loss='mean_absolute_error')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_upr = model_upr.fit(
#     X_train_upr,
#     y_train_upr,
#     batch_size = 64,
#     epochs=40,
#     verbose=1,
#     validation_split = 0.3
#     )

model_upr.summary()

"""Функция для построения графика потерь модели на тренировочной и тестовой выборках"""

def model_loss_plot(model_history):
    plt.figure(figsize=(10, 5))
    plt.plot(model_history.history['loss'])
    plt.plot(model_history.history['val_loss'])
    plt.title('График потерь модели', size=12)
    plt.ylabel('Средняя абсолютная ошибка', size=12)
    plt.xlabel('Эпоха', size=12)
    plt.legend(['loss', 'val_loss'], loc='best')
    plt.show()

"""Функция для построения графика оригинального и предсказанного значения у"""

def actual_and_predicted_plot(original_y, predicted_y):    
    plt.figure(figsize=(10,5))
    plt.title('Тестовые и прогнозные значения', size=12)
    plt.plot(original_y, color='blue', label = 'Тестовые значения')
    plt.plot(predicted_y, color='red', label = 'Прогнозные значения')
    plt.legend(loc='best')
    plt.show()

"""Функция для построения точечного графика оригинального и предсказанного значения у"""

def actual_and_predicted_scatter(original_y, predicted_y):
    plt.figure(figsize=(10,5))
    plt.title('Рассеяние тестовых и прогнозных значений', size=15)
    plt.scatter(original_y, predicted_y)
    plt.xlabel('Тестовые значения', size=12)
    plt.ylabel('Прогнозные значения', size=12)
    plt.show()

model_loss_plot(history_upr)

pred_upr = model_upr.predict(np.array((X_test_upr)))
original_upr = y_test_upr.values
predicted_upr = pred_upr

actual_and_predicted_plot(original_upr, predicted_upr)

actual_and_predicted_scatter(original_upr, predicted_upr)

print(f'Model MAE: {model_upr.evaluate(X_test_upr, y_test_upr, verbose=1)}')

print(f'MAE среднего значения: {np.mean(np.abs(y_test_upr-np.mean(y_test_upr)))}')

"""Нейронная сеть для прогноза прочности при растяжении"""

X_train_pr_norm = normalizer.adapt(np.array(X_train_pr))

model_pr = Sequential(X_train_pr_norm)

model_pr.add(Dense(128))
model_pr.add(BatchNormalization())
model_pr.add(LeakyReLU())
model_pr.add(Dense(64))
model_pr.add(BatchNormalization())
model_pr.add(LeakyReLU())
model_pr.add(Dense(64))
model_pr.add(BatchNormalization())
model_pr.add(LeakyReLU())
model_pr.add(Dense(32))
model_pr.add(BatchNormalization())
model_pr.add(LeakyReLU())
model_pr.add(Dense(1))
model_pr.add(Activation('selu'))

early_pr = EarlyStopping(monitor='val_loss', min_delta=0, patience=20, verbose=1, mode='auto')

model_pr.compile(
    optimizer=tf.optimizers.SGD(learning_rate=0.01),
    loss='mean_absolute_error'
    )

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_pr = model_pr.fit(
#     X_train_pr,
#     y_train_pr,
#     batch_size = 32,
#     epochs=300,
#     verbose=1,
#     validation_split = 0.3,
#     callbacks=[early_pr])

model_pr.summary()

model_loss_plot(history_pr)

pred_pr = model_pr.predict(np.array((X_test_pr)))
original_pr = y_test_pr.values
predicted_pr = pred_pr

actual_and_predicted_plot(original_pr, predicted_pr)

actual_and_predicted_scatter(original_pr, predicted_pr)

print(f'Model MAE: {model_pr.evaluate(X_test_pr, y_test_pr)}')

print(f'MAE среднего значения: {np.mean(np.abs(y_test_pr-np.mean(y_test_pr)))}')

"""Нейронная сеть для предсказания соотношения матрица-наполнитель"""

x_mn = df.drop(['Соотношение матрица-наполнитель'], axis=1)
y_mn = df[['Соотношение матрица-наполнитель']]

X_train_mn, X_test_mn, y_train_mn, y_test_mn = train_test_split(x_mn, y_mn, test_size=0.3, random_state=1)

X_train_mn_norm = normalizer.adapt(np.array(X_train_mn))

model_mn = Sequential(X_train_mn_norm)

model_mn.add(Dense(128))
model_mn.add(BatchNormalization())
model_mn.add(LeakyReLU())
model_mn.add(Dense(128, activation='selu'))
model_mn.add(BatchNormalization())
model_mn.add(Dense(64, activation='selu'))
model_mn.add(BatchNormalization())
model_mn.add(Dense(32, activation='selu'))
model_mn.add(BatchNormalization())
model_mn.add(LeakyReLU())
model_mn.add(Dense(16, activation='selu'))
model_mn.add(BatchNormalization())
model_mn.add(Dense(1))
model_mn.add(Activation('selu'))

early_mn = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')

model_mn.compile(
    optimizer=tf.optimizers.SGD(learning_rate=0.02, momentum=0.5),
    loss='mean_absolute_error')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_mn = model_mn.fit(
#     X_train_mn,
#     y_train_mn,
#     batch_size = 64,
#     epochs=100,
#     verbose=1,
#     validation_split = 0.3,
#     callbacks = [early_mn]
#     )

model_mn.summary()

model_loss_plot(history_mn)

pred_mn = model_mn.predict(np.array((X_test_mn)))
original_mn = y_test_mn.values
predicted_mn = pred_mn

actual_and_predicted_plot(original_mn, predicted_mn)

actual_and_predicted_scatter(original_mn, predicted_mn)

print(f'Model MAE: {model_mn.evaluate(X_test_mn, y_test_mn)}')

print(f'MAE среднего значения: {np.mean(np.abs(y_test_mn-np.mean(y_test_mn)))}')

"""Приложение"""

import pickle

pickle.dump(model_mn, open('model_mn.pkl', 'wb'))

model_load = pickle.load(open('model_mn.pkl', 'rb'))

model_load.predict(X_test_mn)

pred_mn

"""Прогнозные значения изнаально обученной модели совпадают с прогнозными значениями загруженной модели """