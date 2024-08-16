CHAT_EXPORTS := $(wildcard chat-exports/*.json)

LAST_BAD_MESSAGES_FOR_USER ?= 30
LAST_GOOD_MESSAGES ?= 5000

TRAIN_DIR ?= ./train

$(CHAT_EXPORTS): %.json:
	echo running
	python3 ./model-preparation/good-extract.py $@ 	$(TRAIN_DIR)/good 	$(LAST_GOOD_MESSAGES)
	python3 ./model-preparation/sgrana.py $@ 		$(TRAIN_DIR)/bad 	$(LAST_BAD_MESSAGES_FOR_USER)

all: $(CHAT_EXPORTS)
	echo $(CHAT_EXPORTS)
	echo split here dataset