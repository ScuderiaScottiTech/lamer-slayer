import sys

bad_user_commands = ["/ban", ".ban", "/warn", ".warn", "/mute", ".mute", "/regime", ".regime", "/saliera", ".saliera"]

def filter_message(message: str, strip_emoji=False):
    message = message \
        .replace('\n', '') \
        .strip() \
        
    if strip_emoji:
        message = message \
        .encode('latin-1', 'ignore') \
        .decode('latin-1')
    
    return message

banned_types = ['code', 'link', 'pre', 'mention']
def get_text(msg):
    composed = ""
    if type(msg["text"]) is list:
        for element in msg["text"]:
            if type(element) is str:
                composed += element
            elif type(element) is dict:
                # ignore code segments and links
                if element['type'] in banned_types:
                    continue

                composed += element["text"]
            else:
                print("cannot determine type of element", type(element), msg)
                sys.exit(1)
    else:
        composed = msg["text"]

    return composed