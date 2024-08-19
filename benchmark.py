import os
import tensorflow as tf
import numpy as np
import keras

model = tf.saved_model.load("./models/model.tf")
model_forward = model.signatures["serving_default"]

test = [
    "quanto lunghe sono queste stringhe?",
    "Ciao ragazzi ho installato kali sapete come si hackera un wifi??",
    "Conoscete il linguaggio c++?",
    "Conoscete il linguaggio di programmazione Rust? Sembra interessante e nuovo.",
    "Sto programmando un'applicazione in NextJS ma non funziona come inteso.",
    "Vorrei imparare ad usare Electron ma attualmente mi mancano i fondamenti di JS e React. Come consigliate di iniziare?",
    "Sapete entrare in account instagram?",
    "Meglio kali o parrot?",
    "Meglio blackarch o parrot?",
    "Come listo tutti i file in una directory su linux?",
    "ciao ragazzi, vorrei installare ubuntu in dual boot da utilizzare come suite pronta per veloci penetration tests automatizzati, è una buona idea?",
    "Ciao a tutti",
    "Un messaggio generico",
    "Vendo cc carte di credito tutto",
    "cerco hash milano",
    "vendo log esselunga"
]
evaluation = model_forward(tf.constant(test))['output_0']

labels = {}
for label, folder in enumerate(os.listdir("train/")):
    labels[label] = folder
    print(f"Considering {folder} as {label}")

softmax = keras.layers.Softmax()
for prediction, test in zip(evaluation, test):
    softmaxed = softmax(prediction)
    predicted_label = np.argmax(softmaxed)

    predicted_label = labels[predicted_label]

    print("Test", test, "| predicted", predicted_label, "| with percentages of", softmaxed.numpy())
