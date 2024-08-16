import json, sys, os

# args:
# 1) directory di json
# 2) numero messaggi pre /ban

chat_export_dir = sys.argv[1]
MSG_PRE_BAN = int(sys.argv[2])

adminIds = [
    # "user680674121",    #spat
    # "user160598362",    #pietrodev vecchio
    # "user6640826178",   #pietrodev nuovo
    # "user242808656",    #godde 
    # "user399555502",    #notty
    # "user1412637208",   #alpha
    # "user374247068",    #exploiter
    # "channel1445413335" #lol
    #infosec
    "user5666776330",
    "user228641220",
    "user231705046"
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
for file in os.listdir(chat_export_dir):
    f = open(chat_export_dir+file, "r")
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
                        bannedUsersMessageIds.append(msg["reply_to_message_id"])
            else:
                for banCommand in banDotCommands:
                    if banCommand in msg["text"] and msg["reply_to_message_id"] not in bannedUsersMessageIds:
                        bannedUsersMessageIds.append(msg["reply_to_message_id"])

    lastIndex = 0
    bad_counter = 0
    for msg in data["messages"]:
        #per quando spat trolla
        if msg["type"] != "service" and msg["id"] in bannedUsersMessageIds and msg["from_id"] not in adminIds:
            bannedUsersIds_Index.append((msg["from_id"], msg["id"], lastIndex))
            bannedUsersIds.append(msg["from_id"])
            bad_counter += 1
            print(msg)
        lastIndex += 1

    # f_tot = open("bad/bad.txt", "w")
    for (userId, msgId, lastIndex) in bannedUsersIds_Index:
        curr_numpreban = 0
        iters = 0
        while curr_numpreban < MSG_PRE_BAN and lastIndex >= 1 and iters < 1000:
            if data["messages"][lastIndex]["type"] != "service" and data["messages"][lastIndex]["from_id"] == userId:
                f = open("bad/bad"+str(filecounter_index)+".txt", "w")
                f.write(str(data["messages"][lastIndex]["text"]) + '\n')
                # f_tot.write(str(data["messages"][lastIndex]["text"]) + '\n')
                curr_numpreban += 1
                filecounter_index += 1
                f.close()
            lastIndex -= 1
            # iters += 1 # Uncommentare se si vuole prendere solo messaggi recenti max 1000 dal ban
    # f_tot.close()

# Prendi gli ultimi N messaggi dalla fine di scuderia esclusi i messaggi che precedono un ban
# o messaggi blacklistati
# def containsBlacklist(text):
#     for word in blacklist:
#         if word in text:
#             return True
#     return False
# NUM_GOOD_MSG = fc
# NUM_GOOD_MSG = 6000
# f_tot = open("good/good.txt", "w")
# c=0
# lastIndex = 467908
# while lastIndex > (467908-NUM_GOOD_MSG):
#     if data["messages"][lastIndex]["type"] != "service":
#         if data["messages"][lastIndex]["from_id"] not in bannedUsersIds and data["messages"][lastIndex]["text"] != "" and data["messages"][lastIndex]["text"] != "\n" and not containsBlacklist(data["messages"][lastIndex]["text"]):
#             f = open("good/good"+str(c)+".txt", "w")
#             f.write(str(data["messages"][lastIndex]["text"]) + '\n')
#             f_tot.write(str(data["messages"][lastIndex]["text"]) + '\n')
#             f.close()
#     lastIndex -= 1
#     c+=1
# f_tot.close()

# print("Tot bad:", counter)
