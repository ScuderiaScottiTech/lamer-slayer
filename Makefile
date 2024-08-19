GOOD_CHATS := $(wildcard chat-exports/good/*.json)
BAD_CHATS  := $(wildcard chat-exports/bad/*.json)

NUM_MSG_PRE_BAN := 25

TRAIN_DIR ?= ./train

clean:
	rm -rf $(TRAIN_DIR)/**

$(GOOD_CHATS): %.json:
	python3 ./model-preparation/good-extract.py $@ $(TRAIN_DIR)

$(BAD_CHATS): %.json:
	python3 ./model-preparation/bad-extract.py $@ $(TRAIN_DIR) $(NUM_MSG_PRE_BAN)

all: clean $(GOOD_CHATS) $(BAD_CHATS)