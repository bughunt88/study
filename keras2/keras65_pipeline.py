# 61번을 파이프라인으로 구성!

import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()


# 1. 데이터 / 전처리

from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train)  
y_test = to_categorical(y_test)

x_train = x_train.reshape(60000, 28*28).astype('float32')/255.
x_test = x_test.reshape(10000, 28*28).astype('float32')/255.


# 2. 모델

def bulid_model(drop=0.5, optimizer='adam'):
    
    inputs = Input(shape=(28*28,), name='Input')
    x = Dense(512, activation='relu', name='Hidden1')(inputs)
    x = Dropout(drop)(x)
    x = Dense(256, activation='relu', name='Hidden2')(inputs)
    x = Dropout(drop)(x)
    x = Dense(128, activation='relu', name='Hidden2')(inputs)
    x = Dropout(drop)(x)
    outputs = Dense(10, activation='softmax', name='outputs')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=optimizer, metrics=['acc'], loss='categorical_crossentropy')
    
    return model


def create_hyperparameters():
    batches = [10,20,30,40,50]
    optimizers = ['rmsprop', 'adam', 'adadelta']
    dropout = [0.1,0.2,0.3]
    return {'kerasclassifier__batch_size': batches, "kerasclassifier__optimizer":optimizers, "kerasclassifier__drop":dropout}

hyperparameters = create_hyperparameters()
model2 = bulid_model()


from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline



from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
model2 = KerasClassifier(build_fn=bulid_model, verbose=1)

model2 = make_pipeline(MinMaxScaler(), model2)
# make_pipeline, pipeline 둥 다 사용가능!


from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

search = RandomizedSearchCV(model2, hyperparameters, cv=3)
# search = GridSearchCV(model2, hyperparameters, cv=3)


search.fit(x_train,y_train)
# 파이프 라인은 verbose=1 같은 다른 파라미터를 사용할 수 없다!
# 이전 KerasClassifier에서 처리해서 넘길 것

print("#################################")

print(search.best_params_)

print(search.best_score_)

print("#################################")


acc = search.score(x_test, y_test)
print("최종 스코어 : ", acc)