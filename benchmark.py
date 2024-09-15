import os
import tensorflow as tf
import numpy as np
import keras
from scipy.stats import entropy

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
    "vendo log esselunga",
    "se avete log eurospin scrivetemi in privato",
    "scrivetemi in pm per droga",
    "le espressioni consteval sono permesse nei template?",
    "qual è l'equivalente dei trait bounds su altri linguaggi?",
    "cerco fumo scambio con cc scrivetemi pm",
    "vendo gift card, logs, tutto fresh scrivetemi pm",
    "come specifico i lifetime parameters su una funzione?",
    "conoscete framework per creare webapp responsive in javascript?",
    "sapete entrare negli account instagram qui?",
    "io di solito uso i generics un po' per tutto come pietrodev anche quando non servono, voi?",
    "cerco droga a torino"
]

models_path = "./models/multiclass2.tf"
labels = {}
softmax = keras.layers.Softmax()

for label, folder in enumerate(os.listdir("train/")):
    labels[label] = folder
    print(f"Considering {folder} as {label}")

# for n, model_name in enumerate(os.listdir(models_path)):
#     print(f"------------------------------\nUsing model{n}: {model_name}")
#     tf.keras.backend.clear_session()
#     model = tf.saved_model.load(models_path+model_name)

print(f"------------------------------\nUsing model{models_path}")
model = tf.saved_model.load(models_path)
model_forward = model.signatures["serving_default"]
evaluation = model_forward(tf.constant(test))['output_0']

for prediction, test in zip(evaluation, test):
    softmaxed = softmax(prediction)
    pred_entropy = entropy(softmaxed)

    predicted_label = np.argmax(softmaxed)
    predicted_label = labels[predicted_label]

    print("Test", test, "| predicted", predicted_label, "| entropy:", round(pred_entropy, 3), "| with percentages of", softmaxed.numpy())
