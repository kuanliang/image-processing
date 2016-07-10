import pandas as pd
import numpy as np

from DataIO import csvToDf
import os

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
    return finalDf