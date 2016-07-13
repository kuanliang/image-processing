from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer, RobustScaler
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
from sklearn.metrics import classification, confusion_matrix

def logistic(X, y, random_state=0):
    
    pipe = Pipeline(
        [
            ('imputer', Imputer(missing_values='NaN', strategy='median', axis=1)),
            ('scaler', RobustScaler()),
            ('clf', linear_model.LogisticRegression(penalty='l1'))
        ]
    )
    param_grid = {
        #'clf__penalty': ('l1'),
        'clf__tol': (1, 1e-1, 1e-2, 1e-3, 1e-4),
        'clf__C': (10, 5, 1, 0.1, 0.01, 0.001, 0.0001)
    }
    
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(mlDf.iloc[:,0:-1], mlDf['label'], test_size = 0.3, random_state=0)
    
    gs_cv = grid_search.GridSearchCV(pipe, param_grid, scoring='f1_weighted')
    
    gs_cv.fit(X_train, y_train)
    
    y_predict = gs_cv.predict(X_test)
    
    return gs_cv
    











