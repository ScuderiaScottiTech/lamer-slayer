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
    "channel1445413335" #lol
    #infosec
    # "user5666776330",
    # "user228641220",
    # "user231705046"
]
banSlashCommands = [
    "/mute",
    "/ban",
    "/regime",
    "/saliera"
]
banDotCommands = [
    ".mute",
    ".ban",
    ".regime",
    ".saliera"
]

filecounter_index = 0
f = open(filename, "r")
data = json.load(f)
f.close()

bannedUsersMessageIds = []
bannedUsersIds_Index = []
bannedUsersIds = []

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

# f_tot = open("bad/bad.txt", "w")
messages = {}
for (userId, msgId, lastIndex) in bannedUsersIds_Index:
    curr_numpreban = 0
    iters = 0
    while curr_numpreban < MSG_PRE_BAN and lastIndex >= 1 and iters < 1000:
        if data["messages"][lastIndex]["type"] != "service" and data["messages"][lastIndex]["from_id"] == userId:
            text = filter.get_text(data["messages"][lastIndex])
            if text != "":
                messages[data["messages"][lastIndex]["id"]] = {"message": text, "userid": data["messages"][lastIndex]["from_id"]}
            curr_numpreban += 1
            filecounter_index += 1
        lastIndex -= 1
        # iters += 1 # Uncommentare se si vuole prendere solo messaggi recenti max 1000 dal ban
# f_tot.write(str(messages))
# f_tot.close()

split.split_into_files(output_directory, os.path.basename(filename), messages)  