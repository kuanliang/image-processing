from DataIO import csvToDf
import pandas as pd

from Transform import align_x_y_theta

import os

dfList = csvToDf('./tear')

frames = []
for df, fileName in dfList:
    print fileName
    fileItems = os.path.splitext(fileName)[0].split('_')
    status = fileItems[0]
    component = '_'.join(fileItems[2:])
    condition = 'tear'
    
    dfAligned = align_x_y_theta(df, component, condition, status)
    frames.append(dfAligned)
    
finalDf = pd.concat(frames)
    







