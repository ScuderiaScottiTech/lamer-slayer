from pyrogram import Client,enums
import json
# Create a new Client instance
app = Client("c1vtoccibot")

chat_id="diocane"
# Get administrators
administrators = []
async def main():
    async with app:
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(m)
            data=json.loads(str(m))
            print(data["user"]["username"])
            print(str(data["user"]["id"])+'\n')

app.run(main())


