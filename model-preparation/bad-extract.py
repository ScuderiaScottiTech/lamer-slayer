from itertools import product
import json, sys, os
import filter

filename = sys.argv[1]
output_directory = sys.argv[2]
MSG_PRE_BAN = int(sys.argv[3])
MAX_BACK_ITERS = 1000

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

banCommands = [
    "mute",
    "ban",
    "regime",
    "saliera",
    "warn",
]
prefixes = ['/', '.']

f = open(filename, "r")
data = json.load(f)
f.close()

bannedUserMessageIds_Index = []
bannedUserIds = []

c = -1
for msg in data["messages"]:
    c += 1
    text = filter.get_text(msg)
    if text == "":
        continue

    action = False
    for bc in list(product(prefixes, banCommands)):
        if text.startswith(''.join(bc)):
            action = True
    
    if action and msg["from_id"] in adminIds:
        # Check if reply exists
        reply_to = msg.get("reply_to_message_id", "")
        # Check if repliant is not an admin
        if reply_to != "" and reply_to not in adminIds:
            bannedUserMessageIds_Index.append((reply_to, c))

# Get actual index of repliant message
c = 0
for msg in data["messages"]:
    c += 1
    text = filter.get_text(msg)
    if text == "":
        continue

    if any(repliantBannedMessageId[0] == msg["id"] for repliantBannedMessageId in bannedUserMessageIds_Index):
        bannedUserIds.append((msg["from_id"], c))

splitted = os.path.basename(filename).split('.') # name is label.messages.groupname.json
label = splitted[0]
n_msgs = 0
try:
    os.mkdir(f"{output_directory}/{label}")
except FileExistsError:
    pass

# Push last N messages into file
f = open(f"{output_directory}/{label}/{os.path.basename(os.path.splitext(filename)[0])}.txt", "w")
for (userId, lastBanIndex) in bannedUserIds:
    currPreBanNum = maxIters = 0
    while currPreBanNum < MSG_PRE_BAN and lastBanIndex >= 0 and maxIters < MAX_BACK_ITERS:
        text = filter.get_text(data["messages"][lastBanIndex])
        text = filter.sanitize_message(text, strip_emoji=True)
        if text != "" and any(bannedUserId[0] == data["messages"][lastBanIndex]["from_id"] for bannedUserId in bannedUserIds) and filter.filter_message(text):
            f.write(text+'\n')
            currPreBanNum += 1
            n_msgs += 1
        maxIters += 1
        lastBanIndex -= 1
f.close()

print(f"--> Produced {n_msgs} for {label}")