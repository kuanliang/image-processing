import pandas as pd
import numpy as np

from DataIO import csvToDf
import os
import math

import re


def align_x_y_theta(df, component, condition, status):
    '''align x, y and theta records and add necessary columns
    
    Notes:
    
    Arguments:
        df
        
        component: 
            extract from file name
            
        condition:
            'tear' or 'drop' or 'repeat'
            
        status:
            'new' or 'return' or 'diff'
    
    Return:
        a transformed dataframe 
        
    '''
    indexList = [0]
    indexList.extend(range(1, 33))
    xDf = df.iloc[:, indexList]
    # rename columns names
    # generate a dictionary to rename columns
    renameDict = {x: 'value{}'.format(ind) for ind, x in enumerate(xDf.columns) if ind > 0}
    xDf = xDf.rename(columns=renameDict)
    # add a column to separate between x, y and theta metric
    xDf['metric'] = 'x'
    xDf['condition'] = condition
    xDf['component'] = component
    xDf['status'] = status

    indexList = [0]
    indexList.extend(range(33, 65))
    yDf = df.iloc[:, indexList]
    # rename columns names
    # generate a dictionary to rename columns
    renameDict = {col: 'value{}'.format(ind) for ind, col in enumerate(yDf.columns) if ind > 0}
    yDf = yDf.rename(columns=renameDict)
    # add a column to separate between x, y and theta metric
    yDf['metric'] = 'y'
    yDf['condition'] = condition
    yDf['component'] = component
    yDf['status'] = status

    indexList = [0]
    indexList.extend(range(65, 97))
    thetaDf = df.iloc[:, indexList]
    # rename columns names
    # generate a dictionary to rename columns
    renameDict = {col: 'value{}'.format(ind) for ind, col in enumerate(thetaDf.columns) if ind > 0}
    thetaDf = thetaDf.rename(columns=renameDict)
    # add a column to separate between x, y and theta metric
    thetaDf['metric'] = 'theta'
    thetaDf['condition'] = condition
    thetaDf['component'] = component
    thetaDf['status'] = status
    
    frames = [xDf, yDf, thetaDf]

    resultDf = pd.concat(frames)
    
    resultDf['SN'] = resultDf['SN'].str.replace('____', '')
    
    return resultDf


def combine_df(path, tag):
    dfList = csvToDf(path)

    frames = []
    for df, fileName in dfList:
        # print fileName
        fileItems = os.path.splitext(fileName)[0].split('_')
        status = fileItems[0]
        component = '_'.join(fileItems[2:])
        condition = tag
    
        dfAligned = align_x_y_theta(df, component, condition, status)
        frames.append(dfAligned)
    
    finalDf = pd.concat(frames)
    
    # transform column value1 ~ value32 to numeric (some theta are objects)
    finalDf[['value{}'.format(x) for x in range(1,33)]] = finalDf[['value{}'.format(x) for x in range(1,33)]]\
                                                          .apply(pd.to_numeric)
    
    # add absolute 
    finalDfThetaCopy = finalDf[finalDf['metric'] == 'theta'].copy()
    finalDfThetaCopy[['value{}'.format(x) for x in range(1,33)]] = finalDfThetaCopy[['value{}'.format(x) for x in range(1,33)]].apply(np.abs)
    finalDfThetaCopy['metric'] = 'thetaAbs'
    # append to finalDf
    finalDf = pd.concat([finalDf, finalDfThetaCopy])
    
    return finalDf
    
    
def lineup(df, tag):
    dfFrames = []
    for sn in df['SN']:
        snDf = df[df['SN'] == sn].iloc[:,1:33].T
    
        snDf['SN'] = sn
        snDf.rename(columns={snDf.columns[0]:'value'}, inplace=True)
        snDf.index = range(len(snDf))
        dfFrames.append(snDf)
    finalDf = pd.concat(dfFrames)
    finalDf['metric'] = tag
    return finalDf
    
    
def create_zDf(df):
    dfList = []
    for group in df.groupby('SN'):
        for comGroup in group[1].groupby('component'):
            SN = comGroup[1]['SN'].value_counts().index[0]
            condition = comGroup[1]['condition'].value_counts().index[0]
            component = comGroup[1]['component'].value_counts().index[0]
            status = comGroup[1]['status'].value_counts().index[0]
            xDf = comGroup[1][comGroup[1]['metric'] == 'x'].iloc[:,1:33]
            yDf = comGroup[1][comGroup[1]['metric'] == 'y'].iloc[:,1:33]
            zDf = ((((xDf**2)+(yDf**2)).apply(math.sqrt)).to_frame()).T
            zDf['SN'] = SN
            zDf['condition'] = condition
            zDf['component'] = component
            zDf['status'] = status
            zDf['metric'] = 'z'
            dfList.append(zDf)
    zDiffDf = pd.concat(dfList)
    
    return zDiffDf
    
def lineup(df, **kwargv):
    dfFrames = []
    for sn in df['SN']:
        snDf = df[df['SN'] == sn][['value{}'.format(x) for x in range(1,33)]].T
    
        snDf['SN'] = sn
        snDf.rename(columns={snDf.columns[0]:'value'}, inplace=True)
        snDf.index = range(len(snDf))
        dfFrames.append(snDf)
    finalDf = pd.concat(dfFrames)
    for key in kwargv.keys():
        finalDf[key] = kwargv[key]
    return finalDf
    
    
    
def create_ML_df(df, query=False):
    '''create dataframe for Machine Learning modeling
    
    Notes:
    
    Args: a dataframe from combine_df result
    
    Returns: a dataframe in matrix format for ML modeling
    
    '''
    condiDfList = []
    df['comp_metric'] = df['component'] + '_' + df['metric']
    for groupCondi in df.groupby('condition'):
        SNDfList = []
        for groupSN in groupCondi[1].groupby('SN'):
            columns = groupSN[1]['comp_metric']
            SN = groupSN[0]
            dfList = []
            for i in range(1, 33):
                record = groupSN[1][['value{}'.format(i)]].T
                record.columns = columns
                record.index = ['{}_{}'.format(SN, i)]
                dfList.append(record)
            # if query == True:
            # avg value was added and will also be transformed 
            if query == True:
                record = groupSN[1][['avg']].T
                record.columns = columns
                record.index = ['{}_avg'.format(SN)]
                dfList.append(record)
            
            tempDf = pd.concat(dfList)

            SNDfList.append(tempDf)
        SNAllDf = pd.concat(SNDfList)
        SNAllDf['label'] = groupCondi[0]
        condiDfList.append(SNAllDf)
    mlDf = pd.concat(condiDfList)
    
    return mlDf

def addZDf(df):
    '''return 
    '''
    zDiffDf = create_zDf(df)
    return pd.concat([df, zDiffDf])
    
    
def createQueryDf(combinedDf):
    '''
    '''
    # add z metric
    combinedZDf = addZDf(combinedDf)
    
    # add a 'avg' column
    combinedZDf['avg'] = combinedZDf[['value{}'.format(i) for i in range(1,33)]].mean(axis=1)
    # transform to mlDf
    mlDf = create_ML_df(combinedZDf, query=True)

    return mlDf[mlDf.index.str.contains('avg')]
    





    
    
    