import json

file = open('result.json', 'r')
data = json.load(file)
file.close()

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

bannedUsersMessageIds = []
bannedUsersIds_Index = []
bannedUsersIds = []
counter = 0
blacklist = [
    "esselunga",
    "carding",
    "vaccino",
    "covid"
]
def containsBlacklist(text):
    for word in blacklist:
        if word in text:
            return True
    return False

for msg in data["messages"]:
    #mesaggio deve essere vettore perché lo prende come un comando bot 
    #prendere la prima entry che dev'essere un dizionario
    if "reply_to_message_id" in msg and msg["from_id"] in adminIds:
        if isinstance(msg["text"], list) and isinstance(msg["text"][0], dict):
            for banCommand in banSlashCommands:
                if banCommand in msg["text"][0]["text"]:
                    bannedUsersMessageIds.append(msg["reply_to_message_id"])
        else:
            for banCommand in banDotCommands:
                if banCommand in msg["text"] and msg["reply_to_message_id"] not in bannedUsersMessageIds:
                    bannedUsersMessageIds.append(msg["reply_to_message_id"])

lastIndex = 0
for msg in data["messages"]:
    #per quando spat trolla
    if msg["type"] != "service" and msg["id"] in bannedUsersMessageIds and msg["from_id"] not in adminIds:
        bannedUsersIds_Index.append((msg["from_id"], msg["id"], lastIndex))
        bannedUsersIds.append(msg["from_id"])
        counter += 1
        print(msg)
    lastIndex += 1

# Prendi i precedenti 50 messaggi max dall'id del messaggio in reply del ban
# Quindi cicla all'indietro finché non trova 50 msg or finisce il file (aka siamo a inizio file)
MSG_PRE_BAN = 5

# f_tot = open("bad/bad.txt", "w")
# fc=0
# for (userId, msgId, lastIndex) in bannedUsersIds_Index:
#     c=0
#     giri = 0
#     while c < MSG_PRE_BAN and lastIndex >= 1 and giri < 1000:
#         if data["messages"][lastIndex]["type"] != "service" and data["messages"][lastIndex]["from_id"] == userId:
#             f = open("bad/bad"+str(fc)+".txt", "w")
#             f.write(str(data["messages"][lastIndex]["text"]) + '\n')
#             f_tot.write(str(data["messages"][lastIndex]["text"]) + '\n')
#             c += 1
#             fc += 1
#             f.close()
#         lastIndex -= 1
#     giri += 1
# f_tot.close()

# Prendi gli ultimi N messaggi dalla fine di scuderia esclusi i messaggi che precedono un ban
# o messaggi blacklistati
# NUM_GOOD_MSG = fc
NUM_GOOD_MSG = 6000

f_tot = open("good/good.txt", "w")
c=0
lastIndex = 467908
while lastIndex > (467908-NUM_GOOD_MSG):
    if data["messages"][lastIndex]["type"] != "service":
        if data["messages"][lastIndex]["from_id"] not in bannedUsersIds and data["messages"][lastIndex]["text"] != "" and data["messages"][lastIndex]["text"] != "\n" and not containsBlacklist(data["messages"][lastIndex]["text"]):
            f = open("good/good"+str(c)+".txt", "w")
            f.write(str(data["messages"][lastIndex]["text"]) + '\n')
            f_tot.write(str(data["messages"][lastIndex]["text"]) + '\n')
            f.close()
    lastIndex -= 1
    c+=1
f_tot.close()

print("NIGGER:", counter)
