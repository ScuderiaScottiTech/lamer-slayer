import matplotlib.pyplot as plt
import shutil
import sys
import tensorflow as tf
import random
import shutil
import os

from tensorflow import keras
from keras._tf_keras.keras import layers
from keras._tf_keras.keras import losses

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

print("--------------")
print("Demo of the dataset:")
for text, label in dataset.take(4):
    print(f"- {label}: {text}")

print("--------------")

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

model = tf.keras.Sequential([
    vectorize_layer,

    layers.Embedding(max_features, 320),
    # layers.Dropout(0.5),

    layers.Conv1D(100, 3, activation='relu'),
    # layers.Conv1D(100, 5, activation='relu'),
    # layers.Conv1D(100, 6, activation='relu'),
    layers.GlobalMaxPooling1D(),

    layers.Dropout(0.5),
    layers.Dense(n_labels)
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
history_dict.keys()
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


tf.saved_model.save(model, export_dir="./models/model.tf")

# y_true = np.concatenate([y for x, y in test_ds], axis=0)
# test_predicted = model.predict(test_ds)
# y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# # Compute confusion matrix
# cm = confusion_matrix(y_true, y_pred)

# Plot the confusion matrix
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["BAD", "GOOD"])
# disp.plot(cmap=plt.cm.Blues)
# plt.title("Confusion Matrix")
# plt.show()    

# clr = classification_report(y_true, y_pred)
# print("Classification Report:\n----------------------\n", clr)

# def predict(text):
#     for message in text:
#         print("Considering message:", message)
#         vectorized_text = vectorize_layer(message)
#         result = model.predict(vectorized_text)
#         print("full result: ", result)
#         result = result[0][0]
#         confidence = 0
#         if result >= 0.5:
#             confidence = result*100
#         else:
#             confidence = (1-result)*100
#         print(f"Prediction: {result:.4f}")
#         print(f"Confidence: {confidence:.4f}%")
#         threshold = 0.5
#         predicted_class = (result >= threshold).astype(int)
#         if predicted_class == 0:
#             print("BAD")
#         else:
#             print("GOOD")
#         print("-----------------")

# examples = [
#     ["cerco cc scrivetemi in pm per info"],
#     ["Ciao ragazzi sono Pietro e sviluppo in Rust"],
#     ["Voglio uccidere tutti vi ammazzo uno ad uno"],
#     ["l'unico tossico sei tu chissà che cazzo ti cali per stare messo così"],
#     ["Ho installato Kali ma non so farlo funzionare"],
#     ["Vi faccio vedere il mio progetto su GitHub"],
#     ["Ciao ragazzi cosa ne pensate di nextjs"],
#     ["Ahahah"],
#     ["Andatemi a mettere una star sul progetto"],
#     ["Vaffanculo a tutti"]
# ]
# predict(examples)