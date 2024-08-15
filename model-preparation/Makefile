# Example usage: 
# make dataset-name="50" dir-json="lamer-slayer/chat-exports/" num-msg-preban="5"

move-good: move-bad
	rm -rf ../train/$(dataset-name)/train/good
	rm -rf ../train/$(dataset-name)/test/good
	./mvtraintest.sh good ../train/$(dataset-name)/test/good
	mv good ../train/$(dataset-name)/train/
move-bad: populate
	rm -rf ../train/$(dataset-name)/train/bad
	rm -rf ../train/$(dataset-name)/test/bad
	./mvtraintest.sh bad ../train/$(dataset-name)/test/bad
	mv bad ../train/$(dataset-name)/train/

populate: dir-good
	python sgrana.py $(dir-json) $(num-msg-preban)

dir-good: dir-bad
	rm -rf good
	mkdir good
dir-bad:
	rm -rf bad
	mkdir bad
