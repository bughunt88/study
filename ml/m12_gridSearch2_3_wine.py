
# 최적의 툴을 찾아주는 코드 

import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score

from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


import  warnings
warnings.filterwarnings('ignore')

# 1. 데이터 
dataset = load_wine()
x = dataset.data
y = dataset.target

x_train, x_test, y_train, y_test = train_test_split(x, y,  train_size=0.7, random_state = 77, shuffle=True ) 

kfold = KFold(n_splits=5, shuffle=True)


parameters = [
    {'n_estimators' : [100,200]},
    {'max_depth' : [6,8,10,12]},
    {'min_samples_leaf' : [3,5,7,10]},
    {'n_jobs' : [-1,2,4]}
]




# 2. 모델

model = GridSearchCV(RandomForestClassifier(), parameters, cv=kfold)
# 파라미터 값들(dict 형태)을 모두 돌려주는 코드
# 하나의 모델로 볼 수 있다


# 3. 훈련

model.fit(x_train, y_train)


# 3. 평가, 예측
# score = cross_val_score(model,x_train,y_train, cv=kfold)

print('최적의 매개변수 : ', model.best_estimator_)
# model.best_estimator_ : 위에 파라미터 값을 넣은 것 중 최고를 뽑아서 알려준다 

y_pred = model.predict(x_test)

print('최종정답률 : ', accuracy_score(y_test,y_pred))


# print('모델정답률 : ', model.score(y_test,y_pred))
