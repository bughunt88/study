import numpy as np
import pandas as pd
import tensorflow.keras.backend as K

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score,RandomizedSearchCV, GridSearchCV
from sklearn.metrics import accuracy_score

from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from keras.utils.np_utils import to_categorical
from sklearn.decomposition import PCA
import joblib
from keras.preprocessing.image import ImageDataGenerator,load_img,img_to_array # Image Related
import matplotlib.pyplot as plt


import  warnings
warnings.filterwarnings('ignore')

# 1. 데이터 

train = pd.read_csv('../data/vision/train.csv')
submission = pd.read_csv('../data/vision/submission.csv')
test = pd.read_csv('../data/vision/test.csv')

temp = pd.DataFrame(train)
test_df = pd.DataFrame(test)

x = temp.iloc[:,3:]
y = temp.iloc[:,1]

x = x.to_numpy()
y = y.to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y,  train_size=0.7, random_state = 77, shuffle=True ) 

kfold = KFold(n_splits=5, shuffle=True)

print("시작")

# XGB에 수정했을 시 유의미한 파라미터들 

'''
parameters = [
    {"n_estimators" : [400,500,600], "learning_rate":[0.1,0.001,0.01], "max_depth":[4,5,6,7,8],"colsample_bytree":[0.1,0.3,0.6,0.8,1], "colsample_bylevel":[0.1,0.3,0.6,0.7,0.9]}
    ,{"n_estimators" : [400,500,600], "learning_rate":[0.1,0.001,0.01], "max_depth":[4,5,6,7,9], "colsample_bytree":[0.6,0.7,0.9]},
    {"n_estimators" : [400,500,600], "learning_rate":[0.1,0.001,0.5], "max_depth":[4,5,6,7,8], "colsample_bytree":[0.6,0.9,1], "colsample_bylevel":[0.6,0.7,0.9]}
]
'''

parameters={'booster' :['gbtree'],
                 'silent':[True],
                 "max_depth":[4,5,6,7,8],
                 'min_child_weight':[1,3,5],
                 'gamma':[0,1,2,3],
                 'nthread':[4],
                 "colsample_bytree":[0.1,0.3,0.6,0.8,1],
                 "colsample_bylevel":[0.6,0.7,0.9],
                 'n_estimators':[500],
                 'objective':['binary:logistic'],
                 'random_state':[2],
                 "learning_rate":[0.1,0.001,0.01]
            }





# 2. 모델

model = GridSearchCV(XGBClassifier(n_jobs = 8), parameters, cv=kfold)
# 파라미터 값들(dict 형태)을 모두 돌려주는 코드
# 하나의 모델로 볼 수 있다


# 3. 훈련

model.fit(x_train, y_train, verbose=1, eval_metric=['mlogloss'])

# 3. 평가, 예측
# score = cross_val_score(model,x_train,y_train, cv=kfold)

print('최적의 매개변수 : ', model.best_estimator_)
# model.best_estimator_ : 위에 파라미터 값을 넣은 것 중 최고를 뽑아서 알려준다 

y_pred = model.predict(x_test)

print('최종정답률 : ', accuracy_score(y_test,y_pred))


import joblib
joblib.dump(model, '../data/vision/checkpoint_rs.dat')


print("완료")

# 최종정답률 :  0.5252032520325203

'''
최적의 매개변수 :  XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=0.6,
              colsample_bynode=1, colsample_bytree=0.9, gamma=0, gpu_id=-1,
              importance_type='gain', interaction_constraints='',
              learning_rate=0.1, max_delta_step=0, max_depth=5,
              min_child_weight=1, missing=nan, monotone_constraints='()',
              n_estimators=400, n_jobs=8, num_parallel_tree=1,
              objective='multi:softprob', random_state=0, reg_alpha=0,
              reg_lambda=1, scale_pos_weight=None, subsample=1,
              tree_method='exact', validate_parameters=1, verbosity=None)
'''