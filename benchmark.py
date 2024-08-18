import tensorflow as tf
import numpy as np

model = tf.saved_model.load("./models/model.tf")
model_forward = model.signatures["serving_default"]

test = ["Ho passato Analisi 1", "Ho bisogno di installare KDE", "Come si installa Arch?", "Derivata parziale", "Ciao"]
evaluation = model_forward(tf.constant(test))['output_0']

print(evaluation)

for prediction, test in zip(evaluation, test):
    predicted_label = np.argmax(prediction)

    print("Test", test, "predicted", predicted_label)
