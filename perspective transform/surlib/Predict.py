import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.metrics import accuracy_score
from Plot import plot_probability

def predict_query(mlDf, model, column, plot=False):
    '''predict query according to specified model
    
    Notes: 
    
    Argus:
        mlDf:
        model:
        column:
    
    Return:
        predict result
    
    '''
    predict = model.predict(mlDf[column].iloc[:,0:-1])
    predict_prob = model.predict_proba(mlDf[column].iloc[:,0:-1])
    
    accuracy = accuracy_score(mlDf[column].iloc[:,-1], predict)
    
    print accuracy
    
    plot_probability(mlDf, predict_prob)
    
    return predict, predict_prob