CHATS 		:= $(wildcard chat-exports/*.json)
WHITELIST 	:= chat-exports/scuderia.json

LAST_BAD_MESSAGES_FOR_USER ?= 30
LAST_GOOD_MESSAGES ?= 3000

TRAIN_DIR ?= ./train

clean:
	rm -rf $(TRAIN_DIR)/good
	rm -rf $(TRAIN_DIR)/bad

$(CHATS): %.json:
	python3 ./model-preparation/bad-extract.py $@ $(TRAIN_DIR)/bad $(LAST_BAD_MESSAGES_FOR_USER)

$(WHITELIST): %.json:
	python3 ./model-preparation/bad-extract.py $@ $(TRAIN_DIR)/bad $(LAST_BAD_MESSAGES_FOR_USER)
	python3 ./model-preparation/good-extract.py $@ $(TRAIN_DIR)/good $(LAST_GOOD_MESSAGES)

all: clean $(CHATS) $(WHITELIST)