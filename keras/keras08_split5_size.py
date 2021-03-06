# 실습 train_size / test_size 에 대해 완벽 이해할 것 




from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# 1. 데이터 

x = np.array(range(1,101))
y = np.array(range(1,101))


#x_train = x[:60] # : 앞에 아무것도 없으면 처음부터라고 나타낸다  1 ~ 60
#x_val = x[60:80] # 61 ~ 80
#x_test = x[80:]  # 81 ~ 100
# 리스트의 슬라이싱

#y_train = y[:60] # : 앞에 아무것도 없으면 처음부터라고 나타낸다  1 ~ 60
#y_val = y[60:80] # 61 ~ 80
#y_test = y[80:]  # 81 ~ 100
# 리스트의 슬라이싱


from sklearn.model_selection import train_test_split
# 싸이킷 런에서 스플릿 해주는 기능이 있다 

# x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.2, shuffle=False) 


x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.2, shuffle=False) 


# shuffle=False 은 순서 섞지 말고 나오도록 하는 함수 , 섞고 싶으면 True, 기본 값은 트루이다

print(x_train)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


# 1.1 인 경우 
# ValueError: The sum of test_size and train_size = 1.1, should be in the (0, 1) range. Reduce test_size and/or train_size.
# 이라는 에러가 발생한다 
# train_size + test_size = 0 ~ 1 사이에 값이 나와야 한다

# 0.9 인 경우 
# 데이터가 100개에서 train_size : 0.7 와 test_size : 0.2 로 구해보면 
# train_size의 값은 70개가 나온다 test_size의 값은 20개 나온다
# 100개의 데이터로 나눴지만 70+20개 총 90개 
# 10개의 데이터 손실이 나왔다


# 스칼라 : 하나의 숫자를 의미 ( 0차원 )
# ex) 10 
# 백터 : 스칼라의 배열 ( 1차원 )
# ex) [10], [10,], [10,20,30]
# 행렬 : 2차원의 배열 ( 2차원 )
# ex) [[10,20,30],[1,2,3,4]]
# 텐서 : 2차원 이상의 배열 ( 다차원 )
# ex) [  [ [10,20] , [1,2,3] ],[ [4,5,6] , [7,8,9] ]  ]


# 배치 사이즈에 대하여 정리 
# 모델의 가중치를 한번 업데이트시킬 때 사용되는 샘플들의 묶음을 의미합니다.
# 만약에 총 1000개의 훈련 샘플이 있는데, 배치 사이즈가 20이라면 20개의 샘플 단위마다 모델의 가중치를 한번씩 업데이트시킵니다. 총 50번(=1000/20) 가중치가 업데이트 됨



'''

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, shuffle=False)

print(x_train.shape)
print(x_val.shape)
print(y_train.shape)
print(y_val.shape)





print(x_val)
print(y_val)

print("########")
print(x_train.shape)
print(x_val.shape)

print(y_train.shape)
print(y_val.shape)


# 2. 모델 구성

model = Sequential()
model.add(Dense(5, input_dim = 1))

model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(10))

model.add(Dense(1))

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit(x_train, y_train, epochs=100, validation_data=(x_val, y_val))

# 4. 평가, 예측

loss, mae = model.evaluate(x_test, y_test)

y_predict = model.predict(x_test)

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



# shuffle = False
# loss :  0.021176215261220932
# mae :  0.14000539481639862

# shuffle = True
# loss :  0.0024943221360445023
# mae :  0.04311959445476532

# validation = 0.2
# loss :  0.004702096339315176
# mae :  0.05939912796020508


'''