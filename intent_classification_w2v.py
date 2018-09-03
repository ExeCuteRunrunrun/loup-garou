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
word_index      = tokenizer.word_index

sequences       = tokenizer.texts_to_sequences(X_train) #mode='tfidf')
X_train_enc     = pad_sequences(sequences, maxlen=30)
seque_test      = tokenizer.texts_to_sequences(X_test) #mode='tfidf')
X_test_enc      = pad_sequences(seque_test, maxlen=30)

def modelquora(pretrained_path="sgns.zhihu.word"):
    dic_quora = {}
    with open(pretrained_path, "r", encoding="utf-8", errors='ignore') as list_words:

        for line_word in list_words:
            if not line_word or line_word.isspace() or line_word.startswith("#"): continue
            list_line = line_word.split()
            dic_quora[list_line[0]] = np.asarray(list_line[1:], dtype='float32')
        #print(self.dic_wiki["grand"].shape)
    return dic_quora

def embeddingMarix(word_index,vocabulary_size=5000, EMBEDDING_DIM=300):
    dic_quora = modelquora()
    embedding_matrix = np.zeros((vocabulary_size, EMBEDDING_DIM))
    for word, i in word_index.items():
        embedding_vector = dic_quora.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    return embedding_matrix

embedding_matrix = embeddingMarix(word_index, EMBEDDING_DIM=300)

## create model
model_w2v = Sequential()
model_w2v.add(Embedding(vocabulary_size, 300, input_length=30, weights=[embedding_matrix], trainable=False))
model_w2v.add(Dropout(0.2))
model_w2v.add(LSTM(100))
model_w2v.add(Dense(8, activation='sigmoid'))
model_w2v.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# checkpointer = ModelCheckpoint(filepath="/w2v_b50_mlen30_d02_e50.hdf5", verbose=1, save_best_only=True)
# callbackss = [checkpointer] # permission denied
## Fit train data
model_w2v.fit(X_train_enc, y_train_enc,batch_size=batch_size, validation_split=0.1, epochs=3)#, callbacks=callbackss)

### Evaluate the model
score = model_w2v.evaluate(X_test_enc, y_test_enc,
                       batch_size=batch_size, verbose=1)

print('Test accuracy:', score[1])

### Save Tokenizer i.e. Vocabulary
with open('tokw2v_b50_mlen30_d02_e50.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

model_w2v.model.save('w2v_b50_mlen30_d02_e50.h5')
labels = encoder.classes_
print(labels)

### Load model and tokenizer
model_w2v = load_model('w2v_b50_mlen30_d02_e50.h5')
# model_w2v = Sequential()
# model_w2v.add(Embedding(5000, 300, input_length=30))
# model_w2v.add(LSTM(300, dropout=0.2, recurrent_dropout=0.2))
# model_w2v.add(Dense(8, activation='sigmoid'))
# model_w2v.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model_w2v.load_weights('w2v_b50_mlen30_d02_e50.h5')


with open('tokw2v_b50_mlen30_d02_e50.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

x_data = "我 也 觉得 很 奇怪，你 这个 3号 为什么 要去 聊 5号 和 9号 呢。你 是个 民 的话 你 绝对 不会 找 女巫。在我看来 3号 狼面 很大，因为 他 在 这个 位置 去 找神，让我 觉得 他 不是 个 好身份。我 认 5号 7号 好身份，9号 跳 女巫，我 还是 比较 可以 接受 的吧。今晚 出 这个 3号".split('。')

x_data_series = pd.Series(x_data)

x_tokenized = tokenizer.texts_to_sequences(x_data_series)#, mode='tfidf')
# print(x_tokenized)
x_pad       = pad_sequences(x_tokenized, maxlen=30)


for x in x_pad:
    prediction = model_w2v.predict(np.array([x]))
    predicted_label = labels[np.argmax(prediction[0])]
    print("Predicted label: " + predicted_label, x)
