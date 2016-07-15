from bokeh.charts import BoxPlot, show
from bokeh.models import HoverTool
from Transform import lineup
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt

import numpy as np


def plot_box(df, component):
    dfComp = df[df['component'] == component]
    dfComp_x = dfComp[dfComp['metric'] == 'x']
    dfComp_y = dfComp[dfComp['metric'] == 'y']
    dfComp_t = dfComp[dfComp['metric'] == 'theta']
    finalxDf = lineup(dfComp_x, 'x')
    finalyDf = lineup(dfComp_y, 'y')
    finaltDf = lineup(dfComp_t, 'theta')
    frames = [finalxDf, finalyDf, finaltDf]
    
    xytDf = pd.concat(frames)
    
    p = BoxPlot(xytDf, values='value', label=['SN', 'metric'], color='SN', legend=None, title=componentb)
    #p.add_tools(HoverTool())
    show(p)
    

from bokeh.charts import BoxPlot, show
from bokeh.models import HoverTool


def plot_all_box(df, component, labelList, outliers=True, **labelFilter):
    '''plot box plots for comparing variation between different conditions
    
    Notes: 
    
    Args: 
        df: the dataframe generated by combined_df
        component: location on the board
        labelList: a list containing label group showed on the box plot (x axis)
        outliers: True or False
        **labelFilter: keyword argument to specify which record to be included, such as 
                       metric='x' => only show x metric
    
    Return: box plot 
    '''
    
    dfComp = df[df['component'] == component]

    # replaced by list comprehension below

    # dfComp_x_drop = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'drop')]
    # dfComp_y_drop = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'drop')]
    # dfComp_z_drop = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'drop')]
    # dfComp_t_drop = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'drop')]
    # finalxdropDf = lineup(dfComp_x_drop, metric='x', condition='drop')
    # finalydropDf = lineup(dfComp_y_drop, metric='y', condition='drop')
    # finalzdropDf = lineup(dfComp_z_drop, metric='z', condition='drop')
    # finaltdropDf = lineup(dfComp_t_drop, metric='theta', condition='drop')
    
    
    # dfComp_x_tear = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'tear')]
    # dfComp_y_tear = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'tear')]
    # dfComp_z_tear = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'tear')]
    # dfComp_t_tear = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'tear')]
    # finalxtearDf = lineup(dfComp_x_tear, metric='x', condition='tear')
    # finalytearDf = lineup(dfComp_y_tear, metric='y', condition='tear')
    # finalztearDf = lineup(dfComp_z_tear, metric='z', condition='tear')
    # finalttearDf = lineup(dfComp_t_tear, metric='theta', condition='tear')
    
    # dfComp_x_dup = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'duplicate')]
    # dfComp_y_dup = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'duplicate')]
    # dfComp_z_dup = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'duplicate')]
    # dfComp_t_dup = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'duplicate')]
    # finalxdupDf = lineup(dfComp_x_dup, metric='x', condition='duplicate')
    # finalydupDf = lineup(dfComp_y_dup, metric='y', condition='duplicate')
    # finalzdupDf = lineup(dfComp_z_dup, metric='z', condition='duplicate')
    # finaltdupDf = lineup(dfComp_t_dup, metric='theta', condition='duplicate')

    # return finalxdropDf but replaced by following script triggered by input df
    #metrics = ['x', 'y', 'z', 'theta', 'thetaAbs']
    metrics = [metric for metric in df['metric'].value_counts().index]
    
    # conditions =['drop', 'tear', 'duplicate'] replaced by following script triggered by input df
    conditions = [condition for condition in df['condition'].value_counts().index]
    
    frames = [lineup(dfComp[(dfComp['metric'] == metric) & (dfComp['condition'] == condition)], metric=metric, condition=condition)\
        for condition in conditions for metric in metrics]
    
    #frames = [finalxdupDf, finalydupDf, finalzdupDf, finaltdupDf, finalxtearDf, finalytearDf, finalztearDf, finalttearDf,\
    #          finalxdropDf, finalydropDf, finalzdropDf, finaltdropDf]
    
    xyztDf = pd.concat(frames)
    
    xyztFilteredDf = xyztDf.copy()
    for key in labelFilter.keys():
        xyztFilteredDf = xyztFilteredDf[xyztFilteredDf[key] == labelFilter[key]]
    
    # return xyztDf
    # return xytDf
    # p = BoxPlot(xytDf, values='value', label=['condition', 'metric', 'SN'], legend=None, color='condition', title=component)
    # p = BoxPlot(xyztDf, values='value', label=labelList, color=labelList[0], outliers=outliers, title=component)
    p = BoxPlot(xyztFilteredDf, values='value', label=labelList, color=labelList[0], outliers=outliers, title=component)
    #p.add_tools(HoverTool())
    # output_file("condition.html")
    show(p)
    
def plot_confusion_matrix(true, predict, title='Confusion matrix', cmap=plt.cm.Blues, size=24):
    '''plot confusion matrix according to true and predict values
    
    Note:
    
    Args:
        true
        predict
        title
        comp
        size
    
    Return: None
    
    '''
    
    cm = confusion_matrix(true, predict)
    cmReal = cm.copy()
    cmRecall = np.around(cm.astype(float) / cm.sum(axis=0), 2)
    cmPrecision = np.around(cm.astype(float) / cm.sum(axis=1), 2)
    cmF = (cmRecall * cmPrecision * 2) / (cmRecall + cmPrecision)
    
    # figure(figsize = (20, 20))
    cm=cmF.copy()
    plt.figure(figsize=(10,10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, size=20)
    plt.colorbar()
    # tick_marks = np.arange(3)
    plt.xticks(np.arange(3), [u"drop", u"Normal", u"Tear"], rotation=45, size=20)
    plt.yticks(np.arange(3), [u"drop", u"Normal", u"Tear"], size=20)
    plt.tight_layout()
    plt.ylabel(u"Actual class", size=20)
    plt.xlabel(u"Predicted class", size=20)
    
    ax = plt.gca()
    ax.grid(False)
    for i in range(3):
        for j in range(3):
            if cm[i][j] != 0:
                ax.text(j, i, 'P:{},C:{}\n({})'.format(cmPrecision[i][j],\
                                                       cmRecall[i][j],\
                                                       cmReal[i][j]),\
                                                       fontsize=15,color='gray',\
                                                       horizontalalignment='center',\
                                                       verticalalignment='center',)
    