import pandas as pd
import numpy as np
import math

data1=pd.read_csv('datasets/ProcessedData/data1.1.csv')
data2=pd.read_csv('datasets/ProcessedData/data2.1.csv')
data3=pd.read_csv('datasets/ProcessedData/data3.1.csv')
data4=pd.read_csv('datasets/ProcessedData/data4.1.csv')
data5=pd.read_csv('datasets/ProcessedData/data5.1.csv')


data = pd.concat([data1,data2,data3,data4,data5], axis=0)
len(data)

cols = data.columns
temp = data[cols].values.flatten()

s = pd.Series(temp)
s = s.str.strip()
s = s.values.reshape(data.shape)

data = pd.DataFrame(s, columns=data.columns)

symptoms=pd.read_csv('datasets/ProcessedData/Symptoms.csv')
symptoms.head()

oneHotEncoding = []
for x in range(len(symptoms)):
    oneHotEncoding.append(symptoms.iloc[x][0])
del oneHotEncoding[2]
print(len(oneHotEncoding))

from datetime import datetime

def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))

start_time = timer(None)
# Time taken: 1 hours 25 minutes and 34.24 seconds.
# Time taken: 1 hours 1 minutes and 18.4 seconds.

array = []
l = len(oneHotEncoding)+1
for x in range(len(data)):
    temp = [0] * l
    temp[0] = data.iloc[x][0]
    for y in range(len(data.iloc[x][:])-1):
        if type(data.iloc[x][y+1]) == type("str"):
          index = oneHotEncoding.index(data.iloc[x][y+1])+1
          temp[index] = 1
    array.append(temp)
            
timer(start_time)
    
col = np.concatenate((['Condition'],oneHotEncoding), axis=0, out=None)
saveData = pd.DataFrame(array, columns=col)
saveData.to_csv('datasets/ProcessedData/oneHotEncodedSymptoms.csv', index = False)
#test=pd.read_csv('datasets/ProcessedData/oneHotEncodedSymptoms.csv')
#test.head()
