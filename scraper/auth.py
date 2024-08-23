from pyrogram import Client

api_id = <api_id>
api_hash = "<api_hash>"
bot_token = "<bot_token>"

app = Client(
    "<application_name>",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()
