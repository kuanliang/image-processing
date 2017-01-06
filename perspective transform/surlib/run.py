# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 14:38:11 2016

@author: Andy
"""

import surlib
import argparse
import subprocess

# specify ap as argument parse parameter
ap = argparse.ArgumentParser()

# E:\SUR\picture\Difference\test\before
ap.add_argument("-b", "--before", help="path to before imange directory")
# E:\SUR\picture\Differernce\test\after
ap.add_argument("-a", "--after", help="path to after image directory")
args = vars(ap.parse_args())

# execute E:\SUR\vision\vision1.0.exe
# this will generate 24 excel files in E:\SUR\DataFile\
visionExe = subprocess.call(["E:/SUR/vision/vision.exe"])

if visionExe == 0:
    # transform excel files to csv
    surlib.xlsToCsv("E:/SUR/vision/DataFile/")
    queryDf = surlib.createQueryDf("E:/SUR/vision/DataFile/", tag='Normal')

    # load the model
    modelCol = surlib.load_model("E:/SUR/model/model_20160718.dump")
    model = modelCol[0]
    columns = modelCol[1]

    predict, predictProb = surlib.predict_query(queryDf, model=model, column=columns)

    predictC = ['Normal' if x == 'duplicate' else x for x in predict]

    assignProb = [predictProb[x].max() for x in range(len(predictProb))]

    for i in range(len(predictC)):
        print '{} was predicted as {} with {} confidence'.format(queryDf.index[i], predictC[i], assignProb[i])


else:
    print 'the vision exe file crashed!!!'



