import json

file = open('scam/result.json', 'r')
data = json.load(file)
file.close()
n=0
messaggi=[]
for msg in data["messages"] and n < 5000:
    text=msg["text"]
    if msg["type"] != "service" and text not in messaggi:
        f=open("bad/"+str(n)+".txt", "w")
        f.write(str(text))
        f.close()
        n+=1