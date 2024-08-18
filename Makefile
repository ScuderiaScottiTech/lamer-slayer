CHATS 		:= $(wildcard chat-exports/*.json)

TRAIN_DIR ?= ./train

clean:
	rm -rf $(TRAIN_DIR)/**

$(CHATS): %.json:
	python3 ./model-preparation/good-extract.py $@ $(TRAIN_DIR)

all: clean $(CHATS) $(WHITELIST)