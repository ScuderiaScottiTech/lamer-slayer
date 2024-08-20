from pyrogram import Client
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated
from pyrogram.types import Message
import asyncio

import tensorflow as tf
import numpy as np
import keras
import os

import db

table_name = "suspicious_users"
OSSERVATION_THRESH = 2
conn, cur = db.establish_connection(table_name)
osservation_user_ids = db.load_db(cur, table_name)

app = Client("c1vtoccibot")

model = tf.saved_model.load("../models/einstein.tf")
model_forward = model.signatures["serving_default"]

print("Loaded DB:", osservation_user_ids)

labels = {}
for label, folder in enumerate(os.listdir("../train/")):
    labels[label] = folder
    print(f"Considering {folder} as {label}")

def predict(text: str) -> tuple[str, any]:
    text = [text]
    softmax = keras.layers.Softmax()
    evaluation = model_forward(tf.constant(text))['output_0']
    softmaxed = softmax(evaluation)
    predicted_label = np.argmax(softmaxed)
    predicted_label = labels[predicted_label]
    return (predicted_label, softmaxed.numpy())

@app.on_chat_member_updated()
async def log(_, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member == None:
        return
    
    user_id = chat_member_updated.from_user.id
    curr_thresh = osservation_user_ids.get(user_id, -1)
    if curr_thresh == -1:
        osservation_user_ids[user_id] = OSSERVATION_THRESH
        db.insert(cur, conn, table_name, user_id, OSSERVATION_THRESH)

@app.on_message(filters.text & filters.group)
async def echo(_, message: Message):
    print(osservation_user_ids)
    user_id = message.from_user.id
    curr_thresh = osservation_user_ids.get(user_id, -1)
    if curr_thresh >= 1:
        osservation_user_ids[user_id] -= 1
        db.update(cur, conn, table_name, user_id, curr_thresh-1)

        (label, pred) = predict(message.text)
        await message.reply(f"La sentenza: {label} con percentuali di {pred}")

app.run()