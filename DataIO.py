import os
import pandas as pd

def csvToDf(path, sep='\t'):
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



