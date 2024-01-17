import random
import nltk
import pickle
import numpy as np
import json
from nltk.stem import WordNetLemmatizer # used for same words like work,worked,works
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Activation,Dropout
from tensorflow.python.keras.optimizer_v2.gradient_descent import SGD


lemetizer = WordNetLemmatizer()
contents = json.loads(open('Database/intents.json').read())

words = []  # contains all words
classes = []  # contains tags
documents = []  # contains linked both word and tag
ignore_letters = ["?", ",", ".", "/", "!"]

for content in contents["intents"]:
    for pattern in content["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)  # adds data as a stack sequence
        documents.append((word_list, content["tag"]))
        if content["tag"] not in classes:
            classes.append(content["tag"])


words = [lemetizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open("Database/words.pkl", "wb"))
pickle.dump(classes, open("Database/classes.pkl", "wb"))

traning =[]
output_empty = [0]*len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemetizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    traning.append([bag, output_row])

random.shuffle(traning)
traning=np.array(traning, dtype=object)

train_x=list(traning[:,0])
train_y=list(traning[:,1])

model=Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))

model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd=SGD(learning_rate=0.01,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])
hist=model.fit(train_x,train_y,epochs=200,batch_size=5,verbose=1)
model.save('Database/Model.h5',hist)



