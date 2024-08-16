from pyrogram import Client, filters

import tensorflow as tf

from tensorflow import keras
from keras._tf_keras.keras import layers
from keras._tf_keras.keras.models import load_model

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

modelpath_30 = 'models/model-30dataset.keras'
modelpath_infosec = 'models/model-infosec5.keras'
modelpath_scam = '/home/spar/code/beef/models/model-scam-150seq.keras'

train_dir_30 = "/home/spar/code/beef/train/30/train"
train_dir_infosec = "/home/spar/code/beef/train/infosec5/train"
train_dir_scam = "/home/spar/code/beef/train/scam/train"

model_30 = load_model(modelpath_30, compile = True)
model_50 = load_model(modelpath_infosec, compile = True)
model_scam = load_model(modelpath_scam, compile = True)

d30_sequence_length = 150 # Dataset30: 150/100, Dataset50: 200/250/150
dinfosec_sequence_length = 200
dscam_sequence_length = 150

batch_size = 32
seed = 42
max_features = 10000
embedding_dim = 16

raw_train_ds_30 = tf.keras.utils.text_dataset_from_directory(
    train_dir_30,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed
)
raw_train_ds_50 = tf.keras.utils.text_dataset_from_directory(
    train_dir_infosec,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed
)
raw_train_ds_scam = tf.keras.utils.text_dataset_from_directory(
    train_dir_scam,
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
    output_sequence_length=dinfosec_sequence_length
)
vectorize_layer_scam = layers.TextVectorization(
    standardize="strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=dscam_sequence_length
)

train_text_30 = raw_train_ds_30.map(lambda x, y: x)
vectorize_layer_30.adapt(train_text_30)
train_text_50 = raw_train_ds_50.map(lambda x, y: x)
vectorize_layer_50.adapt(train_text_50)
train_text_scam = raw_train_ds_scam.map(lambda x, y: x)
vectorize_layer_scam.adapt(train_text_scam)

def vectorize_text_30(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer_30(text), label
def vectorize_text_50(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer_50(text), label
def vectorize_text_scam(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer_scam(text), label

# Returns False if it's BAD, True if it's GOOD
def predict(text):
    text = [text]
    print("Considering message:", text)
    vectorized_text_30 = vectorize_layer_30(text)
    result_30 = model_30.predict(vectorized_text_30)
    result_30 = result_30[0][0]
    confidence_30 = 0
    if result_30 >= 0.5:
        confidence_30 = result_30*100
    else:
        confidence_30 = (1-result_30)*100

    vectorized_text_50 = vectorize_layer_50(text)
    result_50 = model_50.predict(vectorized_text_50)
    result_50 = result_50[0][0]
    confidence_50 = 0
    if result_50 >= 0.5:
        confidence_50 = result_50*100
    else:
        confidence_50 = (1-result_50)*100

    vectorized_text_scam = vectorize_layer_scam(text)
    result_scam = model_scam.predict(vectorized_text_scam)
    result_scam = result_scam[0][0]
    confidence_scam = 0
    if result_scam >= 0.5:
        confidence_scam = result_scam*100
    else:
        confidence_scam = (1-result_scam)*100
    
    print(f"D30 Prediction | Confidence: {result_30:.4f} | {confidence_30:.4f}%")
    print(f"D-Lamer Prediction | Confidence: {result_50:.4f} | {confidence_50:.4f}%")
    print(f"D-Scam Prediction | Confidence: {result_scam:.4f} | {confidence_scam:.4f}%")

    threshold = 0.5
    predicted_class_30 = (result_30 >= threshold).astype(int)
    predicted_class_50 = (result_50 >= threshold).astype(int)
    the_sentence = False
    if predicted_class_30 == 0 or predicted_class_50 == 0:
        print("BAD")
        the_sentence = False
    else:
        print("GOOD")
        the_sentence = True
    print("-----------------")

app = Client("c1vtoccibot")

@app.on_message(filters.text & filters.group)
async def echo(client, message):
    (sentenza, result_30, result_50, result_scam, confidence_30, confidence_50, confidence_scam) = predict(message.text)
    sentenza_text = "BAD"
    if sentenza:
        sentenza_text = "GOOD"
    await message.reply(f"La sentenza: {sentenza_text}\nD30 Prediction | Confidence: {result_30:.4f} | {confidence_30:.4f}%\nD-Lamer Prediction | Confidence: {result_50:.4f} | {confidence_50:.4f}%\nD-Scam Prediction | Confidence: {result_scam:.4f} | {confidence_scam:.4f}%")

app.run()