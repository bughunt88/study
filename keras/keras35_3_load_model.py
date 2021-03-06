import numpy as np
a = np.array(range(1,11))
size = 5

def split_x(seq, size):
    aaa = []
    for i in range(len(seq) - size + 1):     #행
        subset = seq[i : (i+size)]           #열
        aaa.append(subset)
    print(type(aaa))
    return np.array(aaa)

dataset = split_x(a, size)
print(dataset.shape) # (6, 5)

x = dataset[:,:-1]
y  = dataset[:, -1]

print(x.shape) #(6, 4)
print(y.shape) #(6,)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size= 0.8 , shuffle=True, random_state=311)

x = x.reshape(x.shape[0], x.shape[1], 1)
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

#2. 모델구성

# (LSTM모델로 (4,1 필요))
from tensorflow.keras.models import load_model
model = load_model('../data/h5/save_keras35.h5')

model.summary()

#.컴파일 , 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit(x_train, y_train, epochs=100, batch_size=4, validation_split=0.2, verbose=2)

#평가, 예측
loss = model.evaluate(x_test, y_test, batch_size=4)
print('loss: ', loss)

y_predict = model.predict(x_test)

from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print('RMSE: ', RMSE(y_test, y_predict))

from sklearn.metrics import r2_score
R2 = r2_score(y_test, y_predict)
print('R2: ', R2)

# 35-3 모델 불러와서 적용
# loss:  [0.17135117948055267, 0.3046298027038574]
# RMSE:  0.413945866051646
# R2:  0.8286488199787527