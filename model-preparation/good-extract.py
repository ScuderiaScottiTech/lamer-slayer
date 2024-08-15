import json, sys

# TODO:
# Write to file(s) (one for each line, i.e. msg)

bad_user_commands = ["/ban", ".ban", "/warn", ".warn", "/mute", ".mute"]
adminIds = [
    "user680674121",    #spat
    "user160598362",    #pietrodev vecchio
    "user6640826178",   #pietrodev nuovo
    "user242808656",    #godde 
    "user399555502",    #notty
    "user1412637208",   #alpha
    "user374247068",    #exploiter
    "channel1445413335" #lol
]

messages = {}
banned_ids = {}
dataset = json.load(open(sys.argv[1]))

for msg in dataset["messages"]:
    composed = ""
    if type(msg["text"]) is list:
        for element in msg["text"]:
            if type(element) is str:
                composed += element
            elif type(element) is dict:
                composed += element["text"]
            else:
                print("cannot determine type of element", type(element), msg)
                sys.exit(1)
    else:
        composed = msg["text"]

    if "from_id" not in msg:
        continue

    bad_command = ""
    for buc in bad_user_commands:
        if composed.startswith(buc):
            bad_command = buc

    if bad_command != "" and msg["from_id"] in adminIds and "reply_to_message_id" in msg:
        reply_id = msg["reply_to_message_id"]
        if reply_id in messages:
            banned_ids[messages[reply_id]["userid"]] = bad_command

    messages[msg["id"]] = { "message": composed, "userid": msg["from_id"] }

print(banned_ids)