import pandas as pd
import numpy as np
import math
import sys
import tensorflow as tf


data1=pd.read_csv('../datasets/ProcessedData/encodedTargets1.csv')
data2=pd.read_csv('../datasets/ProcessedData/encodedTargets2.csv')
data3=pd.read_csv('../datasets/ProcessedData/encodedTargets3.csv')
data4=pd.read_csv('../datasets/ProcessedData/encodedTargets4.csv')
data5=pd.read_csv('../datasets/ProcessedData/encodedTargets5.csv')
data6=pd.read_csv('../datasets/ProcessedData/encodedTargets6.csv')
data7=pd.read_csv('../datasets/ProcessedData/encodedTargets7.csv')
data8=pd.read_csv('../datasets/ProcessedData/encodedTargets8.csv')
data9=pd.read_csv('../datasets/ProcessedData/encodedTargets9.csv')

data = pd.concat([data1,data2,data3,data4,data5,data6,data7,data8,data9], axis=0)
len(data) #1087273 expected/ revision on len

data = data.drop(['Condition'], axis=1)

dataArray = data.to_numpy()

np.random.shuffle(dataArray)

x = []
y = []
l = len(dataArray[0])
for z in range(len(dataArray)):
    x.append(dataArray[z][:l-1])
    y.append(dataArray[z][l-1])


    
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(4264, activation=tf.nn.softmax))
          
model.compile(optimizer='adam' , loss='sparse_categorical_crossentropy',metrics=['accuracy'])
          
model.fit(np.array(x), np.array(y), batch_size=32, epochs = 4)

model.save('model_4_covid_e.model')
