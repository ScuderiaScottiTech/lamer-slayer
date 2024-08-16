import json, sys
import filter

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

dataset = json.load(open(sys.argv[1]))

messages = {}
banned_ids = {}

for msg in dataset["messages"]:
    composed = filter.get_text(msg) 
    if composed == "" or "from_id" not in msg:
        continue

    # filter out unwanted characters or escapes from text
    composed = filter.filter_message(composed)

    bad_command = ""
    for buc in bad_user_commands:
        if composed.startswith(buc):
            bad_command = buc

    if bad_command != "" and msg["from_id"] in adminIds and "reply_to_message_id" in msg:
        reply_id = msg["reply_to_message_id"]
        if reply_id in messages:
            banned_ids[messages[reply_id]["userid"]] = bad_command

    messages[msg["id"]] = { "message": composed, "userid": msg["from_id"] }

# filter out messages from banned ids
messages = {k: v for k, v in messages.items() if v["userid"] not in banned_ids}
print(messages)