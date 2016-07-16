import os
import pandas as pd
import datetime
import pickle


def csvToDf(path, sep='\t'):
    '''transform csv to python
    
    Notes: 
    
    Args:
        path:
        sep: 
    
    Return: a list containing dataframe extracted from csv files
    
    '''
    # import os
    dirlist = os.listdir(path)
    dfList = []
    for excelfile in dirlist:
        if os.path.splitext(excelfile)[1] == '.csv':
            #print excelfile
            #print path
            filePath = path + excelfile
            #print filePath
            df = pd.read_csv(filePath, sep=sep)
            df.dropna(inplace=True)
            dfList.append((df, excelfile))
    return dfList



def dump_model(model, col, path='./model/'):
    '''pickle dump the model and col to './model/'
    
    Notes: the col is a list containing columns in original order, to make sure that the query is in the same order
    
    Args:
        model: the trained estimator
        col: a python list
    
    Return: a pickle dump file
    '''
    
    # specify the model name, such as model20160711
    fileName = 'model_' + datetime.datetime.now().strftime('%Y%m%d') + '.dump'
    # open a file inputoutput
    filePath = path + '/' + fileName
    fileDump = open(filePath, 'wb')
    # dump the file
    pickle.dump(model, fileDump)
    fileDump.close()

def load_model(path):
    '''load the ML model and its columns
    
    Notes: the dataframe will be loaded also
    
    Args: the path used to load the object (model and columns)
    
    Return:
        model: a scikit learn ML estimator
        mlCol: mlCol list 
    '''
    fileLoad = open(path, 'rb')
    loadObj = pickle.load(fileLoad)
    
    return loadObj[0], loadObj[1]
    

    
    
    
    
    