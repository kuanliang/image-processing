import os
import pandas as pd

def csvToDf(path):
    # import os
    dirlist = os.listdir(path)
    dfList = []
    for excelfile in dirlist:
        if os.path.splitext(excelfile)[1] == '.csv':
            #print excelfile
            path = './tear/' + excelfile
            dfList.append((pd.read_csv(path, sep=';'), excelfile))
    return dfList


