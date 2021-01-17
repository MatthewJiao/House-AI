import tensorflow as tf
import numpy as np
import pandas as pd

import re
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#nltk.download('averaged_perceptron_tagger')
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Embedding, Conv1D, GlobalMaxPooling1D, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from numpy import array
from numpy import argmax

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from mlxtend.plotting import plot_confusion_matrix

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import matplotlib.pyplot as plt
import seaborn as sns

#cleans up the text 
def clean (text):
    text = text.replace('.', '   ') #replaces periods with triple space
    text = re.sub(r'\s\s+', '  ', text) #removes extra spaces and replaces with double space'
    text = text.lower()
    text = re.sub('[^A-Za-z ]+', '', text) #removes special characters; 
    #print ("text is \n" + text)

    parsed = text.split('  ')
    temp = []
    temp2=""
    for x in parsed:
        temp = x.split()
        for y in temp:
            y = lemmatizer.lemmatize(y, get_wordnet_pos(y) )        # will keep sentences together; will separate \n entered symptoms
            if(y not in stopwords.words('english')):
                temp2 = temp2+" "+y
        if(temp2 != ""):
            temp2 = temp2.strip()
            good.append(temp2)
            temp2 = ""
        #print(x)

#lemmatizer
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

#takes input as \n separated  - lots of whitespace in between symptoms
#or takes input as paragraph form; 

lemmatizer = WordNetLemmatizer() 
parsed = [] 
good = []
#string =  "Coughing       Fever's    1    high blood pressure  is    I    so     face rash   \n cold hands        runny nose    inflammatory feet "
string = "the patient today came in with a high fever and severe cough. He had multiple abrasions as well as a skin rash."
clean (string)
# for x in good:
#     print (x)

##########################################################################################################################################################################

def clean_csv(text):
    # delete stopwords from text
    text = text.lower()
    text = re.sub('[^A-Za-z0-9 ]+', ' ', text) #removes special characters; 
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english')) 
    
    # removes any words composed of less than 2 or more than 21 letters
    text = ' '.join(word for word in text.split() if (len(word) >= 2 and len(word) <= 21))

    #lemmatizes
    text = ' '.join([lemmatizer.lemmatize(word,get_wordnet_pos(word)) for word in text.split()])
  #  text = ' '.join(text)
    #text = ' '.join([stemmer.stem(word) for word in text.split()])
    text = text.strip()

    return text


# The maximum number of words to be used. (most frequent)
vocab_size = 50000

# Dimension of the dense embedding.
embedding_dim = 128

# Max number of words in each complaint.
max_length = 10

# Truncate and padding options
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

dataset = pd.read_csv('Symptoms_Good1.csv')

col = ['symptom', 'phrase']
dataset= dataset[col]

dataset['phrase'] = dataset['phrase'].apply(clean_csv)

#dataset = dataset.sample(frac=1)
#dataset = shuffle(dataset)
print('hi')
phrases = dataset["phrase"].values
symptoms = dataset["symptom"].values

print (phrases)

X_train, y_train, X_test, y_test = train_test_split(phrases ,symptoms , test_size = 0.20)
print(X_train.shape,X_test.shape)
print(y_train.shape,y_test.shape)

tokenizer = Tokenizer(num_words=vocab_size, oov_token='<OOV>')
tokenizer.fit_on_texts(X_train)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
print (dict(list(word_index.items())[0:10]))

train_seq = tokenizer.texts_to_sequences(X_train)
train_padded = pad_sequences(train_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)

validation_seq = tokenizer.texts_to_sequences(y_train)
validation_padded = pad_sequences(validation_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
# print('Shape of data tensor:', train_padded.shape)
# print('Shape of data tensor:', validation_padded.shape)

encode = OneHotEncoder()
X_test = X_test.reshape(-1, 1)
y_test = y_test.reshape(-1, 1)

training_labels = encode.fit_transform(X_test)
validation_labels = encode.transform(y_test)

# print(encode.categories_)

training_labels = training_labels.toarray()
validation_labels = validation_labels.toarray()
# print(training_labels)
# print(validation_labels)
###################################################################################################
# model = keras.Sequential()
# model.add(keras.layers.Embedding(88000, 16))
# model.add(keras.layers.GlobalAveragePooling1D())
# model.add(keras.layers.Dense(16, activation="relu"))
# model.add(keras.layers.Dense(74, activation="softmax"))
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# epochs = 500
# batch_size = 32

# class myCallback(tf.keras.callbacks.Callback):
#         def on_epoch_end(self, epoch, logs = {}):
#                 if(logs.get('accuracy')>.999):
#                         print("\nReached 99% accuracy")
#                         self.model.stop_training = True

# #creating an instance of this class to be called on later
# callbacks = myCallback()     

# history = model.fit(train_padded, training_labels ,
#                     epochs=epochs, steps_per_epoch=8,  
#                     batch_size=batch_size, verbose = 1,  
#                     callbacks=[callbacks])

class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs = {}):
                if(logs.get('accuracy')>.85):
                        print("\nReached 92% accuracy")
                        self.model.stop_training = True

#creating an instance of this class to be called on later
callbacks = myCallback()     

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=train_padded.shape[1]))

model.add(Conv1D(48, 5, activation='relu', padding='valid'))
model.add(GlobalMaxPooling1D())
model.add(Dropout(0.5))

model.add(Flatten())
#model.add(Dropout(0.5))

model.add(Dense(736, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) #test and keep testing see which works best; maybe take out dropout

epochs = 300
batch_size = 32

history = model.fit(train_padded, training_labels ,
                    epochs=epochs, batch_size=batch_size, verbose = 1, callbacks = [callbacks])

#model = keras.models.load_model('symptoms_model.h5')
model.save("symptoms_model4good.h5")

# def review_encode(s):
# 	encoded = [1]

# 	for word in s:
# 		if word.lower() in word_index:
# 			encoded.append(word_index[word.lower()])
# 		else:
# 			encoded.append(2)

# 	return encoded
print (word_index)
print (encode.categories_)
print ('\n\n\n')
new_complaint = ["Pseudobulbar Palsy"]
seq = tokenizer.texts_to_sequences(new_complaint)
print(seq)
padded = pad_sequences(seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
print(padded)
pred = model.predict(padded)
acc = model.predict_proba(padded)
predicted_label = encode.inverse_transform(pred)
#print (word_index)
print(encode.inverse_transform(pred))

print('')
print(f'Product category id: {np.argmax(pred[0])}')
print(f'Predicted label is: {predicted_label[0]}')
print(f'Accuracy score: { acc.max() * 100}')
print(f'Predicted label2 is: {predicted_label}')

