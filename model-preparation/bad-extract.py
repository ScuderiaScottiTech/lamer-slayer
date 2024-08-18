import json, sys, os
import filter, split

# args:
# 1) nome dataset .json
# 2) output directory
# 3) num messaggi dell'utente che precedono /ban

filename = sys.argv[1]
output_directory = sys.argv[2]
MSG_PRE_BAN = int(sys.argv[3])

adminIds = [
    "user680674121",    #spat
    "user160598362",    #pietrodev vecchio
    "user6640826178",   #pietrodev nuovo
    "user242808656",    #godde 
    "user399555502",    #notty
    "user1412637208",   #alpha
    "user374247068",    #exploiter
    "channel1445413335", #lol
    "user233411725", # jacopo tediosi
    "user231705046", #kezi
    # "user"
    #infosec
    "user5666776330",
    "user228641220",
    "user231705046",
    "user337885031",
    "user30572916",
    "user5424622807",
    "user1886971377",
]
banSlashCommands = [
    "/mute",
    "/ban",
    "/regime",
    "/saliera",
    "/warn",
]
banDotCommands = [
    ".mute",
    ".ban",
    ".regime",
    ".saliera",
    ".warn"
]



filecounter_index = 0
f = open(filename, "r")
data = json.load(f)
f.close()

bannedUsersMessageIds = []
bannedUsersIds_Index = []

# bannedUsersIds = {}
bannedUsersIds = []
messages = {}
# for msg in data["messages"]:
#     text = filter.get_text(msg)

#     if text == "":
#         continue

#     bc = False
#     for bad_command in filter.bad_user_commands:
#         if text.startswith(bad_command):
#             bc = True
    
#     if bc and msg["from_id"] in adminIds:
#         reply_to = msg.get("reply_to_message_id", "")
#         banned_message = messages.get(reply_to, None)
#         if banned_message != None and reply_to != "":
#             bannedUsersIds[banned_message["userid"]] = reply_to

#     userid = msg["from_id"].strip("user")
#     messages[msg["id"]] = { "message": text, "userid": userid }

# bad_messages = {}
# for user_id, message_id in bannedUsersIds.items():
#     bad_messages |= {id: messages[id] for id in range(int(message_id) - MSG_PRE_BAN, int(message_id)) if id in messages and messages[id]["userid"] == user_id }

for msg in data["messages"]:
    #mesaggio deve essere vettore perché lo prende come un comando bot 
    #prendere la prima entry che dev'essere un dizionario
    if "reply_to_message_id" in msg and msg["from_id"] in adminIds:
        if isinstance(msg["text"], list) and isinstance(msg["text"][0], dict):
            for banCommand in banSlashCommands:
                if banCommand in msg["text"][0]["text"]:
                    text = filter.get_text(msg)
                    if text != "":
                        bannedUsersMessageIds.append(msg["reply_to_message_id"])
        else:
            for banCommand in banDotCommands:
                if banCommand in msg["text"] and msg["reply_to_message_id"] not in bannedUsersMessageIds:
                    text = filter.get_text(msg)
                    if text != "":
                        bannedUsersMessageIds.append(msg["reply_to_message_id"])
                        
lastIndex = 0
bad_counter = 0
for msg in data["messages"]:
    #per quando spat trolla
    if msg["type"] != "service" and msg["id"] in bannedUsersMessageIds and msg["from_id"] not in adminIds:
        bannedUsersIds_Index.append((msg["from_id"], msg["id"], lastIndex))
        bannedUsersIds.append(msg["from_id"])
        bad_counter += 1
    lastIndex += 1

f_tot = open(output_directory+'/'+str(os.path.basename(filename)), "w")
messages = {}
for (userId, msgId, lastIndex) in bannedUsersIds_Index:
    curr_numpreban = 0
    iters = 0
    while curr_numpreban < MSG_PRE_BAN and lastIndex >= 1 and iters < 1000:
        if data["messages"][lastIndex]["type"] != "service" and data["messages"][lastIndex]["from_id"] == userId:
            text = filter.get_text(data["messages"][lastIndex])
            text = filter.sanitize_message(text, strip_emoji=True)
            if text != "" and filter.filter_message(text):
                messages[data["messages"][lastIndex]["id"]] = {"message": text, "userid": data["messages"][lastIndex]["from_id"]}
                f_tot.write(text+'\n')
            curr_numpreban += 1
            filecounter_index += 1
        lastIndex -= 1
        # iters += 1 # Uncommentare se si vuole prendere solo messaggi recenti max 1000 dal ban
# f_tot.write(str(messages))
f_tot.close()

# split.split_into_files(output_directory, os.path.basename(filename), messages)  