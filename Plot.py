from bokeh.charts import BoxPlot, show
from bokeh.models import HoverTool
from Transform import lineup
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook

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
    dfComp = df[df['component'] == component]
    
    dfComp_x_drop = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'drop')]
    dfComp_y_drop = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'drop')]
    dfComp_z_drop = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'drop')]
    dfComp_t_drop = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'drop')]
    finalxdropDf = lineup(dfComp_x_drop, metric='x', condition='drop')
    finalydropDf = lineup(dfComp_y_drop, metric='y', condition='drop')
    finalzdropDf = lineup(dfComp_z_drop, metric='z', condition='drop')
    finaltdropDf = lineup(dfComp_t_drop, metric='theta', condition='drop')
    
    
    dfComp_x_tear = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'tear')]
    dfComp_y_tear = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'tear')]
    dfComp_z_tear = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'tear')]
    dfComp_t_tear = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'tear')]
    finalxtearDf = lineup(dfComp_x_tear, metric='x', condition='tear')
    finalytearDf = lineup(dfComp_y_tear, metric='y', condition='tear')
    finalztearDf = lineup(dfComp_z_tear, metric='z', condition='tear')
    finalttearDf = lineup(dfComp_t_tear, metric='theta', condition='tear')
    
    dfComp_x_dup = dfComp[(dfComp['metric'] == 'x') & (dfComp['condition'] == 'duplicate')]
    dfComp_y_dup = dfComp[(dfComp['metric'] == 'y') & (dfComp['condition'] == 'duplicate')]
    dfComp_z_dup = dfComp[(dfComp['metric'] == 'z') & (dfComp['condition'] == 'duplicate')]
    dfComp_t_dup = dfComp[(dfComp['metric'] == 'theta') & (dfComp['condition'] == 'duplicate')]
    finalxdupDf = lineup(dfComp_x_dup, metric='x', condition='duplicate')
    finalydupDf = lineup(dfComp_y_dup, metric='y', condition='duplicate')
    finalzdupDf = lineup(dfComp_z_dup, metric='z', condition='duplicate')
    finaltdupDf = lineup(dfComp_t_dup, metric='theta', condition='duplicate')
    
    # return finalxdropDf
    
    frames = [finalxdupDf, finalydupDf, finalzdupDf, finaltdupDf, finalxtearDf, finalytearDf, finalztearDf, finalttearDf,\
              finalxdropDf, finalydropDf, finalzdropDf, finaltdropDf]
    
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