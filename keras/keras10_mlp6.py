# y 행렬의 컬럼의 수를 모델구성의 아웃풋 노드에 넣어줘야 한다 

# 1:다 mlp

import numpy as np

# 1. 데이터 

x = np.array([ range(100) ])   # 지금은 (1,100) 이다 

y = np.array([range(711,811), range(1,101), range(201,301)])


print(x)

print(x.shape) # (1,100)

x = np.transpose(x)
y = np.transpose(y)

print(x.shape) # (100,1)


from sklearn.model_selection import train_test_split
# 싸이킷 런에서 스플릿 해주는 기능이 있다 

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, shuffle=True, random_state = 66 ) 
# random_state 는 랜덤 단수를 고정하는 것이다 매번 돌릴 시 바뀌면 결과값이 달라져서 사용함 

print(x_train.shape) # (80,3)
print(y_train.shape) # (80,3)


# 2. 모델구성
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(10, input_dim= 1)) 
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(3))   # 아웃풋 결과가 달라지면 여기도 수정해야한다 

# 인풋과 아웃풋의 수는 컬럼으로 나뉘어 진다!!!!


# 3. 컴파일 훈련
model.compile(loss='mse', optimizer='adam', metrics='mae')
model.fit(x_train,y_train, epochs=100, batch_size=1, validation_split=0.2)

# 4. 평가, 예측

loss, mae = model.evaluate(x_test,y_test)

print('loss : ', loss)
print('mae : ', mae)


y_predict = model.predict(x_test)

# *** y_prdict 이랑 y_test 의 shape를 맞춰야 한다 ***

print(y_predict)



# 사이킷런
from sklearn.metrics import mean_squared_error

def RMSE(y_test, y_predict): 
    return np.sqrt(mean_squared_error(y_test, y_predict)) 
    # mean_squared_error는 sklearn에서 mse 만드는 함수 
    # sqrt는 넘파이에 루트 씌우는 함수



print('loss : ', loss)
print('mae : ', mae )


print("RMSE : ", RMSE(y_test, y_predict))
# print("mse : ", mean_squared_error(y_test, y_predict))
print("mse : ", mean_squared_error(y_predict, y_test))



# R2 만드는 법
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_predict)
print("R2 : ", r2)




x_predict  = np.array([101,402])

y_predict = model.predict(x_predict)


print("x_predic : ", y_predict)
