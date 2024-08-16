import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow import keras
from keras._tf_keras.keras import layers
from keras._tf_keras.keras.models import load_model

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

modelpath = 'models/model-0.76875.keras'
dataset_dir = "/home/spar/code/beef/train/"
model = load_model(modelpath, compile = True)

# settings
batch_size = 16
seed = 999
max_features = 10000
sequence_length = 150
embedding_dim = 16

raw_training_dataset = tf.data.experimental.load('models/saved_data/rawtrain')
vectorize_layer = layers.TextVectorization(
    standardize="strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length
)
train_text = raw_training_dataset.map(lambda x, y: x)
vectorize_layer.adapt(train_text)
def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

def predict(text):
    for message in text:
        print("Considering message:", message)
        vectorized_text = vectorize_layer(message)
        result = model.predict(vectorized_text)
        print("full result: ", result)
        result = result[0][0]
        confidence = 0
        if result >= 0.5:
            confidence = result*100
        else:
            confidence = (1-result)*100
        print(f"Prediction: {result:.4f}")
        print(f"Confidence: {confidence:.4f}%")
        threshold = 0.5
        predicted_class = (result >= threshold).astype(int)
        if predicted_class == 0:
            print("BAD")
        else:
            print("GOOD")
        print("-----------------")

examples = [
    ["cerco cc scrivetemi in pm per info"],
    # ["Ragazzi volevo condividere con voi un progetto di Microsoft che si è rivelato ottimo!"],
    ["Ciao ragazzi sono Pietro e sviluppo in Rust"],
    ["Voglio uccidere tutti vi ammazzo uno ad uno"],
    ["l'unico tossico sei tu chissà che cazzo ti cali per stare messo così"],
    ["Ho installato Kali ma non so farlo funzionare"],
    # ["Come entro nel profilo di Gianni Morandi di Instagram"],
    ["Vi faccio vedere il mio progetto su GitHub"],
    ["Ciao ragazzi cosa ne pensate delle equazioni differenziali"],
    ["Ciao ragazzi cosa ne pensate di nextjs"]
]
predict(examples)