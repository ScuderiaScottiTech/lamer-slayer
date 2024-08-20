import matplotlib.pyplot as plt
import shutil
import sys
import tensorflow as tf
import random
import shutil
import os

import keras
from keras import layers
from keras import losses

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

dataset_dir = sys.argv[1]

def load_partial_dataset(directory: str, label: int):
    files = os.listdir(directory)
    files = [f"{directory}/{f}" for f in files]

    for file in files:
        print(f"---> considering dataset {file} with label {label}")

    dataset = tf.data.TextLineDataset(files).map(lambda x: (x, tf.cast(label, tf.int32)))
    return dataset

datasets = []
n_labels = 0
for label, folder in enumerate(os.listdir(dataset_dir)):
    n_labels = label + 1
    print(f"Loading datasets at {dataset_dir}/{folder}")
    dataset = load_partial_dataset(f"{dataset_dir}/{folder}", label)
    datasets.append(dataset)


dataset = datasets.pop()
while len(datasets) > 0:
    dataset = dataset.concatenate(datasets.pop())

# settings
batch_size = 32
max_features = 10000
sequence_length = 150

# shuffle and batch into batch_size sized batches
dataset = dataset.shuffle(dataset.cardinality(), seed=int(random.random()*1000)).batch(batch_size).cache()
cardinality = dataset.cardinality().numpy()
print("Finished loading dataset, output is", dataset, "with cardinality", cardinality)

def dataset_size(dataset):
    return dataset.reduce(0, lambda x,_: x+1).numpy()

# print("--------------")
# print("Demo of the dataset:")
# for text, label in dataset.take(4):
#     print(f"- {label}: {text}")
# print("--------------")

total_size = dataset_size(dataset)

val_ds = dataset.take(total_size*0.25)
train_ds = dataset.skip(total_size*0.25)

test_ds = val_ds.take(total_size*0.25*0.2)
val_ds = val_ds.skip(total_size*0.25*0.2)

total_length = total_size * batch_size
train_length = dataset_size(train_ds) * batch_size
validation_length = dataset_size(val_ds) * batch_size
test_length = dataset_size(test_ds) * batch_size

print("-------------")
print("Data set statistics:")
print("Total dataset size", total_length)
print("--> Train dataset size:", train_length)
print("--> Validation dataset size:", validation_length)
print("--> Test dataset:", test_length)
print("-------------")

vectorize_layer = layers.TextVectorization(
    standardize="lower_and_strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length
)

# get sentences only from training dataset or else
# validation information would leak
sentences = train_ds.map(lambda x, y: x)
vectorize_layer.adapt(sentences)

vocabulary = vectorize_layer.get_vocabulary()
# print(vocabulary)
# def vectorize_text(text, label):
#     text = tf.expand_dims(text, -1) # Punto (stringa) -> Vettore
#     return vectorize_layer(text), label
# dataset = dataset.map(vectorize_text)

VALIDATION_SHARE = 0.3
TEST_SHARE = 0.3

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

model = keras.Sequential([
    vectorize_layer,

    layers.Embedding(max_features, 320),
    layers.Conv1D(100, 3, activation='sigmoid'),
    layers.GlobalMaxPooling1D(),

    layers.Dropout(0.5),
    layers.Dense(n_labels), # Add normalization
    # directly output logits (need softmax activation afterwards)

    # layers.Softmax(),
])

epochs = 40 # 84 is the sweet spot with 50 dataset
model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()
stopping = keras.callbacks.EarlyStopping(monitor="val_loss", patience=3)

print("beginning training")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    callbacks=[stopping],
    epochs=epochs
)

loss, accuracy = model.evaluate(test_ds)
print("Loss: ", loss)
print("Accuracy: ", accuracy)

# model.save("models/model-"+str(accuracy)[:7]+".keras")

history_dict = history.history
keys = history_dict.keys()
acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss, 'b--', label='Training loss')
# plt.plot(epochs, acc, 'bo', label='Training accuracy')
plt.plot(epochs, val_loss, 'g--', label='Validation loss')
plt.plot(epochs, val_acc, 'g', label='Validation accuracy')
plt.plot()
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

print(keys)

tf.saved_model.save(model, export_dir="./models/model.tf")