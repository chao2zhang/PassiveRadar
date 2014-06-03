import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor, ExtraTreesClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.linear_model import LogisticRegression



print("Loading")
x =  np.genfromtxt('roomtest_rssi.csv',delimiter=',')
y = np.genfromtxt('roomtest_p.csv',delimiter=',')
idx = np.array(np.arange(0, 140, 5))
idx = np.concatenate((idx, idx + 1, idx + 2)).reshape(1, 84)[0]
rx = x[idx]
ry = np.concatenate((y, y, y))

idx = np.array(np.arange(0, 140, 5))
idx = np.concatenate((idx + 3, idx + 4)).reshape(1, 56)[0]
tx = x[idx]
ty = np.concatenate((y, y))

def regress(classifier):
    print("Training")
    classifier.fit(rx, ry)
    print("Predicting")
    hy = classifier.predict(tx)
    d = np.power(np.sum(np.power(hy - ty, 2), axis=1), 0.5)
    print '50%', np.percentile(d, 50)
    print 'Avg', np.mean(d)

def split_regress(c1, c2):
    hy = np.zeros((ty.shape[0],2))
    print("Training")
    c1.fit(rx, ry[:,0])
    print("Predicting")
    hy[:,0] = c1.predict(tx)
    print("Training")
    c2.fit(rx, ry[:,1])
    print("Predicting")
    hy[:,1] = c2.predict(tx)
    d = np.power(np.sum(np.power(hy - ty, 2), axis=1), 0.5)
    print '50%', np.percentile(d, 50)
    print 'Avg', np.mean(d)

regress(RandomForestRegressor(n_estimators=250, random_state=1))

split_regress(GradientBoostingRegressor(n_estimators=250), GradientBoostingRegressor(n_estimators=250))
# classifier = GradientBoostingClassifier(n_estimators=250)
#classifier = LogisticRegression()
split_regress(svm.SVR(), svm.SVR())
