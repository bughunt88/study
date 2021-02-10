
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims
from sklearn.model_selection import StratifiedKFold
from keras import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
import string



# 생각보다 값이 좋지 못함 
# 훈련 데이터의 양은 예전보다 많아짐 대략 a -> 800개 

# 이유 예상 

# 1. 이미지 전처리 문제 
# 2. ImageDataGenerator 파라미터값들 수정
# 3. 모델이 구림

# 하나하나 처리해볼 것


# 문제 발생 

# 훈련 데이터의 값을 1로만 


'''
alphabets = string.ascii_lowercase
alphabets = list(alphabets)
'''


# train 데이터 (1회 대회 train, test 데이터에서 끌어온다)
train = pd.read_csv('../data/vision2/mnist_data/test.csv')
train_a = pd.read_csv('../data/vision2/mnist_data/train.csv')


# *********************
# train 데이터 
# 1회에 쓰던 mnist 데이터 A를 모아서 128으로 리사이징 해준다 
# 알파벳 별로 모델을 만들 것!
tmp1 = pd.DataFrame()

train['y_train'] = 1
train_a['y_train'] = 1

a_train = train.loc[train['letter']=='A']
a_train1 = train_a.loc[train_a['letter']=='A']


a_train1 = a_train1.drop(['id','digit','letter'],1)
a_train = a_train.drop(['id','letter'],1)


tmp1 = pd.concat([a_train,a_train1])

x_train = tmp1.to_numpy().astype('int32')[:,:-1] # (852, 784)
y_train = tmp1.to_numpy()[:,-1] # (852,)


# 이미지 전처리 100보다 큰 것은 254으로 변환, 100보다 작으면 0으로 변환
x_train[100 < x_train] = 254
x_train[x_train < 100] = 0

x_train = x_train.reshape(-1,28,28,1)

# 발리데이션이 필요 없다
# from sklearn.model_selection import train_test_split
# x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,  train_size=0.7, random_state = 66 ) # shuffle False면 섞는다

# 128로 리사이징 
x_train = experimental.preprocessing.Resizing(128,128)(x_train)
#x_val = experimental.preprocessing.Resizing(128,128)(x_val)



# *********************
# test 데이터
# 이번 대회에 주어진 50000개를 test 데이터로 사용해 정확한 모델을 만든다


# 코랩 데이터 
# x_data = np.load('/content/drive/My Drive/mnist/train_data.npy')
# y_data = pd.read_csv('/content/drive/My Drive/mnist/dirty_mnist_2nd_answer.csv')

# 컴터 데이터 
x_data = np.load('../data/vision2/train_data.npy')
y_data = pd.read_csv('../data/vision2/dirty_mnist_2nd_answer.csv')

print(x_data.shape)

y_test = y_data.to_numpy()[:,1] 
x_data = x_data.reshape(-1,128,128,1)

# 128로 리사이징 
x_data = x_data.astype('int32')

x_test = x_data/255.0
x_train = x_train/255.0

# ImageDataGenerator의 값은 더 찾아볼 것!
idg = ImageDataGenerator( 
    
    horizontal_flip=True, # 수평 뒤집기 
    vertical_flip=True, # 수직 뒤집기 
    #width_shift_range=0.1, # 수평 이동
    #height_shift_range=0.1, # 수직 이동
    rotation_range=60, # 회전 
    zoom_range=[0.2,2] # 확대
    
    )
idg2 = ImageDataGenerator()


# *********************
# predict 데이터 넣을 예정
# test_dirty_mnist_2nd 5000개를 x_predict로 사용
# 각 알파벳 별로 0,1을 뽑는다 !!!





train_generator = idg.flow(x_train, y_train, batch_size=16, seed=2020)
test_generator = idg2.flow(x_test, y_test)
# val_generator = idg2.flow(x_val, y_val)

model = Sequential()

model.add(Conv2D(16,(3,3),activation='relu',input_shape=(128,128,1),padding='same'))
model.add(BatchNormalization())

model.add(Conv2D(32,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(32,(5,5),activation='relu',padding='same')) 
model.add(BatchNormalization())
model.add(Conv2D(32,(5,5),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(32,(5,5),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(64,(5,5),activation='relu',padding='same')) 
model.add(BatchNormalization())
model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(BatchNormalization())
 
model.add(Dense(64,activation='relu'))
model.add(BatchNormalization())

model.add(Dense(1,activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.002,epsilon=None),metrics=['acc'])

learning_history = model.fit_generator(train_generator, epochs=100)

model.save('../data/vision2/cp/dacon_a.h5')


loss, acc = model.evaluate(test_generator)
print("loss : ", loss)
print("acc : ", acc)

print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')
print('(ง˙∇˙)ว {오늘 안에 조지고만다!!!]')






x_pred = np.load('../data/vision2/predict_data.npy')

# x_pred = x_pred[2]

x_pred = x_pred.reshape(-1,128,128,1)

x_pred = x_pred/255.0

pred_generator = idg2.flow(x_pred, shuffle=False)

y_predict = model.predict_generator(pred_generator, verbose=True)

print("결과!!!!!!!!!!!!")
print(y_predict)

sub = pd.read_csv('../data/vision2/sample_submission.csv')

sub['a'] = y_predict

sub.to_csv('../data/vision2/file/submission1.csv', index = False)