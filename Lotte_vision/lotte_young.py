import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims
from sklearn.model_selection import StratifiedKFold, KFold
from keras import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam,SGD
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.utils import to_categorical


#데이터 지정 및 전처리
x = np.load("../data/lpd_competition/npy/train_data_x9.npy",allow_pickle=True)
x_pred = np.load('../data/lpd_competition/npy/predict_data9.npy',allow_pickle=True)
y = np.load("../data/lpd_competition/npy/train_data_y9.npy",allow_pickle=True)

x = preprocess_input(x)
x_pred = preprocess_input(x_pred)

idg = ImageDataGenerator(
    width_shift_range=(-1,1),   
    height_shift_range=(-1,1),  
    shear_range=0.2) 


idg2 = ImageDataGenerator()

#y = np.argmax(y, axis=1)

y = to_categorical(y)

from sklearn.model_selection import train_test_split
x_train, x_valid, y_train, y_valid = train_test_split(x,y, train_size = 0.8, shuffle = True, random_state=42)

mc = ModelCheckpoint('../data/lpd_competition/lotte_0317_2.h5',save_best_only=True, verbose=1)

train_generator = idg.flow(x_train,y_train,batch_size=4)
#seed => random_state
valid_generator = idg2.flow(x_valid,y_valid)
test_generator = x_pred

'''
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Flatten, BatchNormalization, Dense, Activation
from tensorflow.keras.applications import VGG19, MobileNet
mobile_net = MobileNet(weights="imagenet", include_top=False, input_shape=(128, 128, 3))
top_model = mobile_net.output
top_model = Flatten()(top_model)
top_model = Dense(512, activation="relu")(top_model)
top_model = Dense(1000, activation="softmax")(top_model)

model = Model(inputs=mobile_net.input, outputs = top_model)
'''

from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Flatten, BatchNormalization, Dense, Activation
efficientnetb7 = EfficientNetB7(include_top=False,weights='imagenet',input_shape=x_train.shape[1:])
efficientnetb7.trainable = True
a = efficientnetb7.output
a = GlobalAveragePooling2D() (a)
a = Flatten() (a)
a = Dense(2028, activation="relu")(a)
a = Dense(1000, activation="softmax")(a)

model = Model(inputs = efficientnetb7.input, outputs = a)


from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
early_stopping = EarlyStopping(patience= 20)
lr = ReduceLROnPlateau(patience= 10, factor=0.5)

model.compile(optimizer=tf.keras.optimizers.Adam(), loss = 'categorical_crossentropy', metrics=['accuracy'])

learning_history = model.fit_generator(train_generator,epochs=100, 
    validation_data=valid_generator, callbacks=[early_stopping,lr,mc])
# predict
model.load_weights('../data/lpd_competition/lotte_0317_2.h5')
result = model.predict(test_generator,verbose=True)
    
print(result.shape)
sub = pd.read_csv('../data/lpd_competition/sample.csv')
sub['prediction'] = np.argmax(result,axis = 1)
sub.to_csv('../data/lpd_competition/sample_001.csv',index=False)