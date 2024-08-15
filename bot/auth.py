from pyrogram import Client

api_id = 24696050
api_hash = "2c94411da7c5ec1936164a57d673f7de"
bot_token = "7512413354:AAHAFo-1VOwI4v3nh44nUqcap8Ri_UTXI1c"

app = Client(
    "c1vtoccibot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()