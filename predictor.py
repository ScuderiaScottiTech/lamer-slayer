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

modelpath_30 = 'models/model-30dataset.keras'
modelpath_50 = 'models/model-infosec5.keras'

train_dir_30 = "/home/spar/code/beef/train/30/train"
train_dir_50 = "/home/spar/code/beef/train/infosec5/train"
batch_size = 32
seed = 42
max_features = 10000
d30_sequence_length = 150 # Dataset30: 150/100, Dataset50: 200/250/150
d50_sequence_length = 250
embedding_dim = 16

model_30 = load_model(modelpath_30, compile = True)
model_50 = load_model(modelpath_50, compile = True)

raw_train_ds_30 = tf.keras.utils.text_dataset_from_directory(
    train_dir_30,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed
)
raw_train_ds_50 = tf.keras.utils.text_dataset_from_directory(
    train_dir_50,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed
)

vectorize_layer_30 = layers.TextVectorization(
    standardize="strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=d30_sequence_length
)
vectorize_layer_50 = layers.TextVectorization(
    standardize="strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=d50_sequence_length
)

train_text_30 = raw_train_ds_30.map(lambda x, y: x)
vectorize_layer_30.adapt(train_text_30)
train_text_50 = raw_train_ds_50.map(lambda x, y: x)
vectorize_layer_50.adapt(train_text_50)

def vectorize_text_30(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer_30(text), label
def vectorize_text_50(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer_50(text), label

def predict(text):
    for message in text:
        print("Considering message:", message)

        vectorized_text_30 = vectorize_layer_30(message)
        result_30 = model_30.predict(vectorized_text_30)
        result_30 = result_30[0][0]
        confidence_30 = 0
        if result_30 >= 0.5:
            confidence_30 = result_30*100
        else:
            confidence_30 = (1-result_30)*100

        vectorized_text_50 = vectorize_layer_50(message)
        result_50 = model_50.predict(vectorized_text_50)
        result_50 = result_50[0][0]
        confidence_50 = 0
        if result_50 >= 0.5:
            confidence_50 = result_50*100
        else:
            confidence_50 = (1-result_50)*100
        
        print(f"D30 Prediction | Confidence: {result_30:.4f} | {confidence_30:.4f}%")
        print(f"D50 Prediction | Confidence: {result_50:.4f} | {confidence_50:.4f}%")
        threshold = 0.5
        predicted_class_30 = (result_30 >= threshold).astype(int)
        predicted_class_50 = (result_50 >= threshold).astype(int)
        if predicted_class_30 == 0 or predicted_class_50 == 0:
            print("BAD")
        else:
            print("GOOD")
        print("-----------------")

examples = [
    ["cerco cc scrivetemi in pm per info"],
    ["Ragazzi volevo condividere con voi un progetto di Microsoft che si è rivelato ottimo!"],
    ["Chi ha log esselunga mi contatti."],
    ["l'unico tossico sei tu chissà che cazzo ti cali per stare messo così"],
    ["se avrò voglia un giorno farò letteralmente il famoso \"rewrite it in rust\" giusto perchè python mi fa schifo tantissimo"],
    ["Ciao se volete investire in bitcoin scrivetemi"],
    ["Ciao propongo metodi di investimento in bitcoin ethereum cryptovalute per investire dm me --> @theinvests32"],
    ["Chi ha log esselunga mi contatti. Free and freeesh @gottoapotto"],
    ["A qualcuno servono doc abbinati con cud/cedolini/f24/cedo pensione/ certificato e contratti vari.. diciamo materiale pesante ja. Offro tutto io FREE AND FRREESHHH"],
    ["raga ma qualcuno sa come si recupera una password di un file rar"],
    ["io ho cercato su internet e sto provando con un attacco brute force numerico"],
    ["ora posso dire di fare parte di una scuderia"],
    ["Mi serve una \"conf\" per \"aggirare i proxy\" per \"fb nfa\""],
    ["esiste merda come fyne perchè esiste merda come tkinter"]
]
predict(examples)