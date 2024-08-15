import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import sys
import tensorflow as tf

from tensorflow import keras
from keras._tf_keras.keras import layers
from keras._tf_keras.keras import losses

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

natural_processing_dir = sys.argv[1]
train_dir = f"{natural_processing_dir}/train"
test_dir = f"{natural_processing_dir}/test"

# settings
batch_size = 32
seed = 42
max_features = 10000
sequence_length = 150
embedding_dim = 16

raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    train_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed
)

print("Label 0 corresponds to", raw_train_ds.class_names[0])
print("Label 1 corresponds to", raw_train_ds.class_names[1])

raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    train_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed
)

raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    test_dir, 
    batch_size=batch_size
)

vectorize_layer = layers.TextVectorization(
    standardize="strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length
)

train_text = raw_train_ds.map(lambda x, y: x)
# OUT_OF_RANGE warning. This is the shit the docs gave to us. "This is expected behavior"
# "adapt() will run until the input dataset is exhausted"
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

model = tf.keras.Sequential([
    layers.Embedding(max_features, embedding_dim),
    layers.Dropout(0.2),
    layers.GlobalAveragePooling1D(),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')]
)
model.summary()

epochs = 75 # 84 is the sweet spot with 50 dataset
model.compile(
    loss=losses.BinaryCrossentropy(),
    optimizer='adam',
    metrics=[tf.metrics.BinaryAccuracy(threshold=0.5)]
)

print("beginning training")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)
loss, accuracy = model.evaluate(test_ds)
print("Loss: ", loss)
print("Accuracy: ", accuracy)

model.save("models/model-"+str(accuracy)[:7]+".keras")

history_dict = history.history
history_dict.keys()
acc = history_dict['binary_accuracy']
val_acc = history_dict['val_binary_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

y_true = np.concatenate([y for x, y in test_ds], axis=0)
y_pred_prob = model.predict(test_ds)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# Compute confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Plot the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["BAD", "GOOD"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

clr = classification_report(y_true, y_pred)
print("Classification Report:\n----------------------\n", clr)

def predict(text):
    for message in text:
        print("Considering message:", message)
        vectorized_text = vectorize_layer(message)
        result = model.predict(vectorized_text)
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
    ["Ragazzi volevo condividere con voi un progetto di Microsoft che si è rivelato ottimo!"],
    ["l'unico tossico sei tu chissà che cazzo ti cali per stare messo così"]
]
predict(examples)