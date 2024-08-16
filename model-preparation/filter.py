import sys

def filter_message(message: str):
    return message \
        .replace('\n', '') \
        .strip() \
        .encode('ascii', 'ignore') \
        .decode('ascii')

def get_text(msg):
    composed = ""
    if type(msg["text"]) is list:
        for element in msg["text"]:
            if type(element) is str:
                composed += element
            elif type(element) is dict:
                # ignore code segments and links
                if element['type'] == 'code' or element['type'] == 'link':
                    continue

                composed += element["text"]
            else:
                print("cannot determine type of element", type(element), msg)
                sys.exit(1)
    else:
        composed = msg["text"]

    return composed