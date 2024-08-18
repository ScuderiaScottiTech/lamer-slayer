import os
import tensorflow as tf
import numpy as np

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
    "Come listo tutti i file in una directory su linux?"
]
evaluation = model_forward(tf.constant(test))['output_0']

for label, folder in enumerate(os.listdir("train/")):
    print(f"Considering {folder} as {label}")

print(evaluation)

for prediction, test in zip(evaluation, test):
    predicted_label = np.argmax(prediction)

    print("Test", test, "predicted", predicted_label)
