#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential,load_model
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.callbacks import ModelCheckpoint

import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

### ==== Read, split, encoding =================
df = pd.read_csv('data_speech_all.csv', sep='\t', encoding='utf-8')
X  = df['segmented']
y  = df['intent']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

### Encode labels
encoder     = LabelBinarizer()
encoder.fit(y_train)
y_train_enc = encoder.transform(y_train)
y_test_enc  = encoder.transform(y_test)

### Create sequence
vocabulary_size = 5000
batch_size      = 50
tokenizer       = Tokenizer(num_words= vocabulary_size, char_level = False)
tokenizer.fit_on_texts(X_train)
# print(tokenizer.word_index)
sequences       = tokenizer.texts_to_sequences(X_train) #mode='tfidf')
X_train_enc     = pad_sequences(sequences, maxlen=30)

seque_test      = tokenizer.texts_to_sequences(X_test) #mode='tfidf')
X_test_enc      = pad_sequences(seque_test, maxlen=30)

### Network architecture
model = Sequential()
model.add(Embedding(5000, 100, input_length=30))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(8, activation='sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
### Train and fit

# checkpointer = ModelCheckpoint(filepath="/weights_b50_mlen30_d02_e50.hdf5", verbose=1, save_best_only=True)
# callbackss = [checkpointer]
model.fit(X_train_enc, y_train_enc,batch_size=batch_size, validation_split=0.1, epochs=3)

### Evaluate the model
score = model.evaluate(X_test_enc, y_test_enc,
                       batch_size=batch_size, verbose=1)

print('Test accuracy:', score[1])

### Save the model
# model.model.save('weights_b50_mlen30_d02_e50.h5') # save all the model, with load_model()
model.save_weights('weights_b50_mlen30_d02_e50.h5') # save only weights, with model.load_weights

### Save Tokenizer i.e. Vocabulary
with open('tok_b50_mlen30_d02_e50.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

labels = encoder.classes_
print(labels)


### Load model and tokenizer
# model = load_model('weights_b50_mlen30_d02_e50.h5')
model = Sequential()
model.add(Embedding(5000, 100, input_length=30))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(8, activation='sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.load_weights('weights_b50_mlen30_d02_e50.h5')


with open('tok_b50_mlen30_d02_e50.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

x_data = "我 也 觉得 很 奇怪，你 这个 3号 为什么 要去 聊 5号 和 9号 呢。你 是个 民 的话 你 绝对 不会 找 女巫。在我看来 3号 狼面 很大，因为 他 在 这个 位置 去 找神，让我 觉得 他 不是 个 好身份。我 认 5号 7号 好身份，9号 跳 女巫，我 还是 比较 可以 接受 的吧。今晚 出 这个 3号".split('。')

x_data_series = pd.Series(x_data)

x_tokenized = tokenizer.texts_to_sequences(x_data_series)#, mode='tfidf')
# print(x_tokenized)
x_pad       = pad_sequences(x_tokenized, maxlen=30)


for x in x_pad:
    prediction = model.predict(np.array([x]))
    predicted_label = labels[np.argmax(prediction[0])]
    print("Predicted label: " + predicted_label)#, x)
