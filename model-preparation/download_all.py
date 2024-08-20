import json
import filter

file = open('../chat-exports/good/scam.2000.json', 'r')
data = json.load(file)
file.close()
n=0
messaggi=[]
f=open("../train/scam/scam.txt", "w")
for msg in data["messages"]:
    if n >= 5000:
        break
    text = filter.get_text(msg)
    if text != "" and msg["type"] != "service" and text not in messaggi:
        f.write(str(text))
        n+=1
f.close()