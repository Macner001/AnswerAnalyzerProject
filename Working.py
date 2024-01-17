import json
import nltk
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.python.keras.models import load_model


lematizer=WordNetLemmatizer()
intents = json.loads(open('Database/intents.json').read())
words = pickle.load(open('Database/words.pkl', 'rb'))
classes = pickle.load(open('Database/classes.pkl', 'rb'))
model = load_model('Database/Model.h5')


def clean_up_sentence(sentance):
    sentence_word=nltk.word_tokenize(sentance)
    sentence_word=[lematizer.lemmatize(word) for word in sentence_word]
    return sentence_word


def bag_of_words(sentance):
    sentence_words=clean_up_sentence(sentance)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentance):
    bow = bag_of_words(sentance)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    result.sort(key=lambda x: x[1], reverse=True)
    return_list=[]
    for r in result:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list


def arrangements(Value,i):
    if len(Value) >= 15:
        Value = predict_class(Value)
        int = Value[0]['intent']
        probability = float(Value[0]['probability'])
        total_marks = intents['intents'][i]['marks']
        if int == intents['intents'][i]['tag']:     # Calculate the answer based on probability
            answer = (probability / 1) * total_marks
            answer = round(answer, 3)
            return answer
        else:
            print("Mis matched")
            answer = 0
            return answer

    else:
        print("Not Complete ")
        answer = 0
        return answer


