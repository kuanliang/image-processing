from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer, RobustScaler
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn import tree
from sklearn import cross_validation
from sklearn import grid_search
from sklearn.metrics import classification, confusion_matrix


import re
import random
import pandas as pd
import numpy as np

def logisticModeling(dfTrain, dfTest, random_state=0):
    '''perform logistic regression
    
    Notes: 
    
    Args:
        dfTrain: training dataframe split according to SN split
        dfTest: testing dataframe split according to SN split

    Return: trained logistic model
    
    '''
    pipe = Pipeline(
        [
            ('imputer', Imputer(missing_values='NaN', strategy='median', axis=1)),
            ('scaler', RobustScaler()),
            ('clf', linear_model.LogisticRegression(class_weight='balanced', max_iter=1000))
        ]
    )
    param_grid = {
        'clf__penalty': ('l1','l2'),
        'clf__tol': (1, 1e-1, 1e-2, 1e-3, 1e-4),
        'clf__C': (10, 5, 1, 0.1, 0.01, 0.001, 0.0001)
    }
    
    
    # X_train, X_test, y_train, y_test = cross_validation.train_test_split(mlDf.iloc[:,0:-1], mlDf['label'], test_size = 0.3, random_state=0)
    
    gs_cv = grid_search.GridSearchCV(pipe, param_grid, scoring='f1_weighted')
    
    X_train, y_train = dfTrain.iloc[:, 0:-1], dfTrain.iloc[:,-1]
    X_test, y_test = dfTest.iloc[:, 0:-1], dfTest.iloc[:, -1]
    
    gs_cv.fit(X_train, y_train)
    
    y_predict = gs_cv.predict(X_test)
    
    return gs_cv, (y_test, y_predict)


def SVMModeling(dfTrain, dfTest, random_state=0):
    
    pipe = Pipeline([
        #('union', InitialProcessor(colInfo=colInfo)),
        ('impute', Imputer(missing_values = 'NaN', strategy = 'median', axis = 1)),
        ('scaler', RobustScaler()),
        #('clf', linear_model.SGDClassifier(loss = 'log', penalty='l1', class_weight='balanced', n_iter=1))
        # ('pca', pca)
        ('clf', SVC(kernel='rbf', class_weight='balanced'))
    ])

    param_grid = {
        'clf__C': (1, 1e2, 1e3, 1e4, 1e5),
        'clf__gamma': (1, 1e-1, 1e-2, 1e-3, 1e-4),
        'clf__tol': (1e-2, 1e-3, 1e-4, 1e-5)
    }
    gs_cv = grid_search.GridSearchCV(pipe, param_grid, scoring='f1_weighted')
    
    X_train, y_train = dfTrain.iloc[:, 0:-1], dfTrain.iloc[:,-1]
    X_test, y_test = dfTest.iloc[:, 0:-1], dfTest.iloc[:, -1]
    
    gs_cv.fit(X_train, y_train)
    
    y_predict = gs_cv.predict(X_test)
    
    return gs_cv, (y_test, y_predict)


def DTModeling(dfTrain, dfTest):
    pipe = Pipeline([
        #('union', InitialProcessor(colInfo=colInfo)),
        ('impute', Imputer(missing_values = 'NaN', strategy = 'median', axis = 1)),
        # ('scaler', RobustScaler()),
        #('clf', linear_model.SGDClassifier(loss = 'log', penalty='l1', class_weight='balanced', n_iter=1))
        # ('pca', pca)
        ('clf', tree.DecisionTreeClassifier())
    ])  

    param_grid = {
        'clf__criterion': ['gini', 'entropy'],
        'clf__max_depth': [3, 4, 5, 6, 7],
        'clf__min_samples_split': [2, 3, 4, 5, 6, 7,  8, 9, 10, 12, 15, 20, 25, 30, 35, 40]}
                  
    gs_cv = grid_search.GridSearchCV(pipe, param_grid, scoring='f1_weighted')
    
    X_train, y_train = dfTrain.iloc[:, 0:-1], dfTrain.iloc[:,-1]
    X_test, y_test = dfTest.iloc[:, 0:-1], dfTest.iloc[:, -1]
    
    gs_cv.fit(X_train, y_train)
    
    y_predict = gs_cv.predict(X_test)
    
    return gs_cv, (y_test, y_predict)

def train_test_split(df, trainRatio=0.6, testRatio=0.4):
    '''split training and testing data according to 3 cases (drop, duplicate, tear)
    
    Notes: the dictionary comprehension is a bit complex, but here are just 3 steps
    
    Args: ML DataFrame
    
    Return: 
        labelSNDictTrain: 
    
    '''
    
    # extract SN of each cases
    labelSNDict = {label: list(set([re.sub('_\d+', '', x) for x in df[df['label'] == label].index]))\
    for label in ['drop', 'duplicate', 'tear']}
    # extract SN for training case of each label
    labelSNDictTrain = {label: random.sample(labelSNDict[label], int(len(labelSNDict[label])*trainRatio))\
    for label in ['drop', 'duplicate', 'tear']}

    # extract training dataframes
    dropTrainDf = pd.concat([df[df.index.str.contains(SN)] for SN in labelSNDictTrain['drop']])
    duplicateTrainDf = pd.concat([df[df.index.str.contains(SN)] for SN in labelSNDictTrain['duplicate']])
    tearTrainDf = pd.concat([df[df.index.str.contains(SN)] for SN in labelSNDictTrain['tear']])
    
    trainDf = pd.concat([dropTrainDf, duplicateTrainDf, tearTrainDf])
    testDf = df.loc[list(set(df.index) - set(trainDf.index))]
    
    
    return trainDf, testDf



