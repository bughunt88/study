
# 컬럼의 중요도를 확인할 수 있는 코드 
# 상관관계랑 비교해서 신뢰할 수 있는 놈으로 결정할 것!

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

# 1. 데이터
dataset = load_boston()

x_train, x_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, train_size = 0.8, random_state=44
)

# 2. 모델
model = DecisionTreeRegressor(max_depth=4)

# 3. 훈련
model.fit(x_train, y_train)

# 4. 평가, 예측
acc = model.score(x_test, y_test)

print(model.feature_importances_)
print("acc : ", acc)


import matplotlib.pyplot as plt
import numpy as np


def plot_feature_importances_dataset(model):
    n_features = dataset.data.shape[1]
    plt.barh(np.arange(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), dataset.feature_names)
    plt.xlabel("Feature Importances")
    plt.ylabel("Features")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()

'''
[0.05832757 0.         0.         0.         0.00572861 0.61409529
 0.00580415 0.09723421 0.         0.         0.01858958 0.00343964
 0.19678095]
acc :  0.8159350178696477
'''