from pyrogram import Client
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated, ChatPermissions, Message
from pyrogram.enums import ChatMemberStatus
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

app = Client("<app_name>")

model = tf.saved_model.load("../models/multiclass2.tf")
model_forward = model.signatures["serving_default"]

print("Loaded DB:", osservation_user_ids)

labels = {}
# for label, folder in enumerate(os.listdir("../train/")):
#     labels[label] = folder
#     print(f"Considering {folder} as {label}")
labels[0] = "dev"
labels[1] = "scam"
labels[2] = "lamer"
bad_labels = ["lamer", "scam"]

def predict(text: str) -> tuple[str, any]:
    text = [text]
    softmax = keras.layers.Softmax()
    evaluation = model_forward(tf.constant(text))['output_0']
    softmaxed = softmax(evaluation)
    predicted_label = np.argmax(softmaxed)
    predicted_label = labels[predicted_label]
    return (predicted_label, softmaxed.numpy())

# 0: Good, 1: Admin intervention, 2: Mute
def take_action(label, pred) -> int:
    if pred.any() > 0.75 and label in bad_labels:
        return 2
    elif label in bad_labels:
        return 1
    return 0

@app.on_chat_member_updated()
async def log(_, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member == None:
        return

    user_id = chat_member_updated.from_user.id
    chat_member = await app.get_chat_member(chat_member_updated.chat.id, user_id)
    if chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return

    curr_thresh = osservation_user_ids.get(user_id, -1)
    if curr_thresh == -1:
        osservation_user_ids[user_id] = OSSERVATION_THRESH
        db.insert(cur, conn, table_name, user_id, OSSERVATION_THRESH)

@app.on_message(filters.text & filters.group)
async def echo(_, message: Message):
    user_id = message.from_user.id
    curr_thresh = osservation_user_ids.get(user_id, -1)
    if curr_thresh >= 1:
        osservation_user_ids[user_id] -= 1
        db.update(cur, conn, table_name, user_id, curr_thresh-1)

        (label, pred) = predict(message.text)
        action = take_action(label, pred)
        match action:
            case 0:
                await message.reply(f"Controllo AI passato.")
            case 1:
                await message.reply(f"@admin intervento richiesto. Categoria risultante: {label} | {pred}")
            case 2:
                await message.reply(f"@admin Controllo AI non passato.\nIl tuo messaggio risulta nella categoria {label} con percentuali di {pred}.\nVerificheremo la decisione al più presto, se ritieni che sia un errore, puoi scrivere a un admin del gruppo.")
                await app.restrict_chat_member(message.chat.id, user_id, ChatPermissions())

app.run()
